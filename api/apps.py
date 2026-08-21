from django.apps import AppConfig

from api.CiStartupTraceEnabled import CiStartupTraceEnabled


class ApiConfig(AppConfig):
    name = "api"

    def ready(self) -> None:
        from api.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        from api.model.uploaded_track.UploadedTrack import UploadedTrack

        CriteriaPlaylistManager.track_playlist_rel_model = TrackPlaylistRel
        CriteriaPlaylistManager.track_model = UploadedTrack

        if CiStartupTraceEnabled.is_tracer_active():
            print(
                "[Django] ApiConfig.ready() - django.setup() finished loading the api app.",
                flush=True,
            )
