from hear.CiStartupTraceEnabled import CiStartupTraceEnabled

if CiStartupTraceEnabled.is_tracer_active():
    print(
        "[Django] hear.models: importing SpotifyArtist / SpotifyLibTrack / User (deep trees; can be slow)...",
        flush=True,
    )

from hear.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from hear.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from hear.model.user.User import User

if CiStartupTraceEnabled.is_tracer_active():
    print("[Django] hear.models: core model imports finished.", flush=True)
    print(
        "[Django] hear.models: Django will now call AppConfig.ready() on each installed app (hear is last).",
        flush=True,
    )

__all__ = ["SpotifyArtist", "SpotifyLibTrack", "User"]
