from django.apps import AppConfig

from hear.CiStartupTraceEnabled import CiStartupTraceEnabled


class HearConfig(AppConfig):
    name = "hear"

    def ready(self) -> None:
        from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

        from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
        from hear.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager
        from hear.model.uploaded_track.UploadedTrack import UploadedTrack
        from hear.model.uploaded_track.UploadedTrackManager import UploadedTrackManager

        CriteriaPlaylistManager.track_playlist_rel_model = TrackPlaylistRel
        CriteriaPlaylistManager.track_model = UploadedTrack
        UploadedTrackManager.criteria_playlist_model = CriteriaPlaylist

        if CiStartupTraceEnabled.is_tracer_active():
            print(
                "[Django] HearConfig.ready() - django.setup() finished loading the hear app.",
                flush=True,
            )
