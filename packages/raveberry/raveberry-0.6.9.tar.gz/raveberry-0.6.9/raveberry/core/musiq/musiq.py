"""This module handles all requests concerning the addition of music to the queue."""

from __future__ import annotations

import logging

import ipware
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import core.musiq.song_utils as song_utils
from core.models import CurrentSong
from core.models import QueuedSong
from core.musiq.localdrive import LocalSongProvider
from core.musiq.music_provider import (
    SongProvider,
    PlaylistProvider,
    MusicProvider,
    WrongUrlError,
    ProviderError,
)
from core.musiq.player import Player
from core.musiq.spotify import SpotifySongProvider, SpotifyPlaylistProvider
from core.musiq.soundcloud import SoundcloudSongProvider, SoundcloudPlaylistProvider
from core.musiq.suggestions import Suggestions
from core.musiq.youtube import (
    YoutubeSongProvider,
    YoutubePlaylistProvider,
)
from core.state_handler import Stateful
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse, JsonResponse
from typing import Any, Dict, Optional, Union, TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from core.base import Base


class Musiq(Stateful):
    """This class provides endpoints for all music related requests."""

    def __init__(self, base: "Base") -> None:
        self.base = base

        self.suggestions = Suggestions(self)

        self.queue = QueuedSong.objects

        self.player = Player(self)
        self.player.start()

    def do_request_music(
        self,
        request_ip: str,
        query: str,
        key: Optional[int],
        playlist: bool,
        platform: str,
        archive: bool = True,
        manually_requested: bool = True,
    ) -> Tuple[bool, str, Optional[int]]:
        """Performs the actual requesting of the music, not an endpoint.
        Enqueues the requested song or playlist into the queue, using appropriate providers.
        Returns a 3-tuple: successful, message, queue_key"""
        providers: List[MusicProvider] = []

        provider: MusicProvider
        if playlist:
            if key is not None:
                # an archived song was requested.
                # The key determines the PlaylistProvider
                provider = PlaylistProvider.create(self, query, key)
                if provider is None:
                    return False, "No provider found for requested playlist", None
                providers.append(provider)
            else:
                # try to use spotify if the user did not specifically request youtube
                if self.base.settings.soundcloud_enabled:
                    soundcloud_provider = SoundcloudPlaylistProvider(self, query, key)
                    if platform == "soundcloud":
                        providers.insert(0, soundcloud_provider)
                    else:
                        providers.append(soundcloud_provider)
                if self.base.settings.spotify_enabled:
                    spotify_provider = SpotifyPlaylistProvider(self, query, key)
                    if platform == "spotify":
                        providers.insert(0, spotify_provider)
                    else:
                        providers.append(spotify_provider)
                if self.base.settings.youtube_enabled:
                    youtube_provider = YoutubePlaylistProvider(self, query, key)
                    if platform == "youtube":
                        providers.insert(0, youtube_provider)
                    else:
                        providers.append(youtube_provider)
        else:
            if key is not None:
                # an archived song was requested.
                # The key determines the SongProvider
                provider = SongProvider.create(self, query, key)
                if provider is None:
                    return False, "No provider found for requested song", None
                providers.append(provider)
            else:
                if platform == "local":
                    # if a local provider was requested,
                    # use only this one as its only possible source is the database
                    providers.append(LocalSongProvider(self, query, key))
                else:
                    if self.base.settings.soundcloud_enabled:
                        try:
                            soundcloud_provider = SoundcloudSongProvider(
                                self, query, key
                            )
                            if platform == "soundcloud":
                                providers.insert(0, soundcloud_provider)
                            else:
                                providers.append(soundcloud_provider)
                        except WrongUrlError:
                            pass
                    if self.base.settings.spotify_enabled:
                        try:
                            spotify_provider = SpotifySongProvider(self, query, key)
                            if platform == "spotify":
                                providers.insert(0, spotify_provider)
                            else:
                                providers.append(spotify_provider)
                        except WrongUrlError:
                            pass
                    if self.base.settings.youtube_enabled:
                        try:
                            youtube_provider = YoutubeSongProvider(self, query, key)
                            if platform == "youtube":
                                providers.insert(0, youtube_provider)
                            else:
                                providers.append(youtube_provider)
                        except WrongUrlError:
                            pass

        if not len(providers):
            return False, "No backend configured to handle your request.", None

        fallback = False
        for i, provider in enumerate(providers):
            try:
                provider.request(
                    request_ip, archive=archive, manually_requested=manually_requested
                )
                # the current provider could provide the song, don't try the other ones
                break
            except ProviderError:
                # this provider cannot provide this song, use the next provider
                # if this was the last provider, show its error
                if i == len(providers) - 1:
                    return False, provider.error, None
                fallback = True
        message = provider.ok_message
        queue_key = None
        if not playlist:
            queue_key = provider.queued_song.id
        if fallback:
            message += " (used fallback)"
        return True, message, queue_key

    def request_music(self, request: WSGIRequest) -> HttpResponse:
        """Endpoint to request music. Calls internal function."""
        key = request.POST.get("key")
        query = request.POST.get("query")
        playlist = request.POST.get("playlist") == "true"
        platform = request.POST.get("platform")

        if query is None or not platform:
            return HttpResponseBadRequest(
                "query, playlist and platform have to be specified."
            )
        ikey = None
        if key:
            ikey = int(key)

        # only get ip on user requests
        if self.base.settings.logging_enabled:
            request_ip, _ = ipware.get_client_ip(request)
            if request_ip is None:
                request_ip = ""
        else:
            request_ip = ""

        successful, message, queue_key = self.do_request_music(
            request_ip, query, ikey, playlist, platform
        )
        if successful:
            return JsonResponse({"message": message, "key": queue_key})
        else:
            return HttpResponseBadRequest(message)

    def request_radio(self, request: WSGIRequest) -> HttpResponse:
        """Endpoint to request radio for the current song."""
        # only get ip on user requests
        if self.base.settings.logging_enabled:
            request_ip, _ = ipware.get_client_ip(request)
            if request_ip is None:
                request_ip = ""
        else:
            request_ip = ""

        try:
            current_song = CurrentSong.objects.get()
        except CurrentSong.DoesNotExist:
            return HttpResponseBadRequest("Need a song to play the radio")
        provider = SongProvider.create(self, external_url=current_song.external_url)
        return provider.request_radio(request_ip)

    @csrf_exempt
    def post_song(self, request: WSGIRequest) -> HttpResponse:
        """This endpoint is part of the API and exempt from CSRF checks.
        Shareberry uses this endpoint."""
        # only get ip on user requests
        if self.base.settings.logging_enabled:
            request_ip, _ = ipware.get_client_ip(request)
            if request_ip is None:
                request_ip = ""
        else:
            request_ip = ""
        query = request.POST.get("query")
        if not query:
            return HttpResponseBadRequest("No query to share.")
        # Set the requested platform to 'spotify'.
        # It will automatically fall back to Youtube
        # if Spotify is not enabled or a youtube link was requested.
        successful, message, _ = self.do_request_music(
            request_ip, query, None, False, "spotify"
        )
        if successful:
            return HttpResponse(message)
        else:
            return HttpResponseBadRequest(message)

    def index(self, request: WSGIRequest) -> HttpResponse:
        """Renders the /musiq page."""
        context = self.base.context(request)
        return render(request, "musiq.html", context)

    def state_dict(self) -> Dict[str, Any]:
        state_dict = self.base.state_dict()
        current_song: Optional[Dict[str, Any]]
        try:
            current_song = model_to_dict(CurrentSong.objects.get())
        except CurrentSong.DoesNotExist:
            current_song = None
        song_queue = []
        all_songs = self.queue.all()
        if self.base.settings.voting_system:
            all_songs = all_songs.order_by("-votes", "index")
        for song in all_songs:
            song_dict = model_to_dict(song)
            song_dict["duration_formatted"] = song_utils.format_seconds(
                song_dict["duration"]
            )
            song_queue.append(song_dict)

        if state_dict["alarm"]:
            state_dict["current_song"] = {
                "queue_key": -1,
                "manually_requested": False,
                "votes": None,
                "internal_url": "",
                "external_url": "",
                "artist": "Raveberry",
                "title": "ALARM!",
                "duration": 10,
                "created": "",
            }
        else:
            state_dict["current_song"] = current_song
        state_dict["paused"] = self.player.paused()
        state_dict["progress"] = self.player.progress()
        state_dict["shuffle"] = self.player.shuffle
        state_dict["repeat"] = self.player.repeat
        state_dict["autoplay"] = self.player.autoplay
        state_dict["volume"] = self.player.volume
        state_dict["song_queue"] = song_queue
        return state_dict
