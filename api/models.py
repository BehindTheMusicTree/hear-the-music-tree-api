import os
import sys

if "pytest" in sys.argv[0] or os.environ.get("ENV") == "ci_test":
    print(
        "[Django] api.models: importing SpotifyArtist / SpotifyLibTrack / User (deep trees; can be slow)...",
        flush=True,
    )

from api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from api.model.user.User import User

if "pytest" in sys.argv[0] or os.environ.get("ENV") == "ci_test":
    print("[Django] api.models: core model imports finished.", flush=True)

__all__ = ["SpotifyArtist", "SpotifyLibTrack", "User"]
