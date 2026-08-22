from hear.CiStartupTraceEnabled import CiStartupTraceEnabled

_URLS_STARTUP_LOG = CiStartupTraceEnabled.is_tracer_active()
if _URLS_STARTUP_LOG:
    print("[Django] hear.urls: importing URLconf (large view/router tree)...", flush=True)

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from hear.utils.AppStaticFileStates import StaticFileStates
from hear.view.AudioMetadataSessionDownloadView import AudioMetadataSessionDownloadView
from hear.view.AudioMetadataSessionView import AudioMetadataSessionView
from hear.view.AudioMetadataView import AudioMetadataView
from hear.view.google_auth import google_auth
from hear.view.spotify_auth import spotify_auth
from hear.view.viewset.model.AllUploadedTracksMixinViewSet import AllUploadedTracksViewSet
from hear.view.viewset.model.SpotifyArtistViewSet import SpotifyArtistViewSet
from hear.view.viewset.model.user.SpotifyUserViewSet import SpotifyUserViewSet

from . import settings
from .view.health import HealthCheckView
from .view.viewset.model.album.AlbumViewSet import AlbumViewSet
from .view.viewset.model.artist.ArtistViewSet import ArtistViewSet
from .view.viewset.model.criteria.children.genre.GenreViewSet import GenreViewSet
from .view.viewset.model.criteria.children.tag.TagViewSet import TagViewSet
from .view.viewset.model.play.PlayViewSet import PlayViewSet
from .view.viewset.model.playlist.children.criteria.genre.GenrePlaylistViewSet import GenrePlaylistViewSet
from .view.viewset.model.playlist.children.criteria.TagPlaylistViewSet import TagPlaylistViewSet
from .view.viewset.model.playlist.children.ManualPlaylistViewSet import ManualPlaylistViewSet
from .view.viewset.model.playlist.PlaylistViewSet import PlaylistViewSet
from .view.viewset.model.SpotifyLibTrackViewSet import SpotifyLibTrackViewSet
from .view.viewset.model.uploaded_track.UploadedTrackViewSet import UploadedTrackViewSet
from .view.viewset.model.user.BaseUserViewSet import BaseUserViewSet
from .view.viewset.SearchViewSet import SearchViewSet

router = routers.DefaultRouter()

router.register(r"users", BaseUserViewSet, basename="user")
router.register(r"spotify-artists", SpotifyArtistViewSet, basename="spotify-artist")

# Do not move PlaylistViewSet after GenrePlaylistViewSet or ManualPlaylistViewSet or it will cause confusion resolving
# reverse urls.
router.register(r"me/spotify", SpotifyUserViewSet, basename="spotify-user")
router.register(r"me/library/uploaded", UploadedTrackViewSet, basename="me-uploaded-track")
router.register(r"me/library/spotify", SpotifyLibTrackViewSet, basename="me-spotify-lib-track")
router.register(r"me/artists", ArtistViewSet, basename="me-artist")
router.register(r"me/albums", AlbumViewSet, basename="me-album")
router.register(r"me/genres", GenreViewSet, basename="me-genre")
router.register(r"me/tags", TagViewSet, basename="me-tag")
router.register(r"me/playlists", PlaylistViewSet, basename="me-playlist")
router.register(r"me/manual-playlists", ManualPlaylistViewSet, basename="me-manual-playlist")
router.register(r"me/genre-playlists", GenrePlaylistViewSet, basename="me-genre-playlist")
router.register(r"me/tag-playlists", TagPlaylistViewSet, basename="me-tag-playlist")
router.register(r"me/plays", PlayViewSet, basename="me-play")

router.register(r"all-tracks", AllUploadedTracksViewSet, basename="all-uploaded-tracks")
router.register(r"search", SearchViewSet, basename="search")

urlpatterns = [
    path(settings.API_ROOT_BASE, include(router.urls)),
    path(settings.API_ROOT_BASE + "audio/metadata/full/", AudioMetadataView.as_view(), name="audio-metadata-full"),
    path(
        settings.API_ROOT_BASE + "audio/metadata/session/",
        AudioMetadataSessionView.as_view(),
        name="audio-metadata-session",
    ),
    path(
        settings.API_ROOT_BASE + "audio/metadata/session-download/",
        AudioMetadataSessionDownloadView.as_view(),
        name="audio-metadata-session-download",
    ),
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path(settings.API_ROOT_BASE + "auth/", include("django.contrib.auth.urls")),
    path(settings.API_ROOT_BASE + "auth/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path(settings.API_ROOT_BASE + "auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(settings.API_ROOT_BASE + "auth/spotify/", spotify_auth, name="api-auth-spotify"),
    path(settings.API_ROOT_BASE + "auth/google/", google_auth, name="api-auth-google"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.STATIC_FILES_STATE in [StaticFileStates.COLLECTING, StaticFileStates.SERVING]:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if _URLS_STARTUP_LOG:
    print("[Django] hear.urls: URLconf import finished.", flush=True)
