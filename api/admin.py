from django.contrib import admin

from .model.album.Album import Album
from .model.all_uploaded_tracks_mixin.AllUploadedTracksMixin import AllUploadedTracksMixin
from .model.artist.Artist import Artist
from .model.criteria.Criteria import Criteria
from .model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel
from .model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from .model.musicbrainz_resource.children.recording.MbRecording import MbRecording
from .model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode,
)
from .model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import MbRecordingMissingCause
from .model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from .model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from .model.playlist.Playlist import Playlist
from .model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from .model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from .model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
from .model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode,
)
from .model.uploaded_track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from .model.uploaded_track.file.TrackFile import TrackFile
from .model.uploaded_track.UploadedTrack import UploadedTrack
from .model.user.admin.UserAdmin import UserAdmin
from .model.user.User import User

admin.site.register(User, UserAdmin)
admin.site.register(UploadedTrack)
admin.site.register(TrackFile)
admin.site.register(FingerprintMissingCause)
admin.site.register(FingerprintMissingCauseCode)
admin.site.register(AllUploadedTracksMixin)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Criteria)
admin.site.register(CriteriaLineageRel)
admin.site.register(Playlist)
admin.site.register(ManualPlaylist)
admin.site.register(CriteriaPlaylist)
admin.site.register(TrackPlaylistRel)
admin.site.register(MbRecording)
admin.site.register(MbRecordingMissingCause)
admin.site.register(MbRecordingMissingCauseCode)
admin.site.register(MbArtist)
admin.site.register(SpotifyLibTrack)
admin.site.register(SpotifyArtist)
