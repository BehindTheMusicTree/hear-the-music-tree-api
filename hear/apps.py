from django.apps import AppConfig

from hear.CiStartupTraceEnabled import CiStartupTraceEnabled


class HearConfig(AppConfig):
    name = "hear"

    def ready(self) -> None:
        from hear.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager
        from hear.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        from hear.model.uploaded_track.UploadedTrack import UploadedTrack

        CriteriaPlaylistManager.track_playlist_rel_model = TrackPlaylistRel
        CriteriaPlaylistManager.track_model = UploadedTrack

        if CiStartupTraceEnabled.is_tracer_active():
            print(
                "[Django] HearConfig.ready() - django.setup() finished loading the hear app.",
                flush=True,
            )
