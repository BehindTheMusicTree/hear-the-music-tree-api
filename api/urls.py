from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.utils.AppStaticFileStates import StaticFileStates
from api.view.viewset.model.AllUploadedTracksMixinViewSet import AllUploadedTracksViewSet
from api.view.spotify_auth import spotify_auth
from api.view.viewset.model.SpotifyArtistViewSet import SpotifyArtistViewSet
from api.view.viewset.model.user.SpotifyUserViewSet import SpotifyUserViewSet

from . import settings
from .view.health import HealthCheckView
from .view.viewset.model.album.AlbumViewSet import AlbumViewSet
from .view.viewset.model.album.ReferenceAlbumViewSet import ReferenceAlbumViewSet
from .view.viewset.model.artist.ArtistViewSet import ArtistViewSet
from .view.viewset.model.criteria.children.genre.GenreViewSet import GenreViewSet
from .view.viewset.model.criteria.children.genre.ReferenceGenreViewSet import ReferenceGenreViewSet
from .view.viewset.model.criteria.children.tag.ReferenceTagViewSet import ReferenceTagViewSet
from .view.viewset.model.criteria.children.tag.TagViewSet import TagViewSet
from .view.viewset.model.artist.ReferenceArtistViewSet import ReferenceArtistViewSet
from .view.viewset.model.play.ReferencePlayViewSet import ReferencePlayViewSet
from .view.viewset.model.play.PlayViewSet import PlayViewSet
from .view.viewset.model.uploaded_track.ReferenceUploadedTrackViewSet import ReferenceUploadedTrackViewSet
from .view.viewset.model.uploaded_track.UploadedTrackViewSet import UploadedTrackViewSet
from .view.viewset.model.playlist.children.criteria.genre.GenrePlaylistViewSet import GenrePlaylistViewSet
from .view.viewset.model.playlist.children.criteria.genre.ReferenceGenrePlaylistViewSet import (
    ReferenceGenrePlaylistViewSet)
from .view.viewset.model.playlist.children.criteria.TagPlaylistViewSet import TagPlaylistViewSet
from .view.viewset.model.playlist.children.criteria.tag.ReferenceTagPlaylistViewSet import ReferenceTagPlaylistViewSet
from .view.viewset.model.playlist.children.ManualPlaylistViewSet import ManualPlaylistViewSet
from .view.viewset.model.playlist.children.ReferenceManualPlaylistViewSet import ReferenceManualPlaylistViewSet
from .view.viewset.model.playlist.PlaylistViewSet import PlaylistViewSet
from .view.viewset.model.playlist.ReferencePlaylistViewSet import ReferencePlaylistViewSet
from .view.viewset.model.SpotifyLibTrackViewSet import SpotifyLibTrackViewSet
from .view.viewset.model.user.BaseUserViewSet import BaseUserViewSet
from .view.viewset.SearchViewSet import SearchViewSet


router = routers.DefaultRouter()

router.register(r'users', BaseUserViewSet, basename='user')
router.register(r'spotify-artists', SpotifyArtistViewSet, basename='spotify-artist')
router.register(r'library/spotify', SpotifyLibTrackViewSet, basename='spotify-lib-track')

# Do not move PlaylistViewSet after GenrePlaylistViewSet or ManualPlaylistViewSet or it will cause confusion resolving
# reverse urls.
router.register(r'me/spotify', SpotifyUserViewSet, basename='spotify-user')
router.register(r'reference/library/uploaded', ReferenceUploadedTrackViewSet, basename='reference-uploaded-track')
router.register(r'reference/artists', ReferenceArtistViewSet, basename='reference-artist')
router.register(r'reference/albums', ReferenceAlbumViewSet, basename='reference-album')
router.register(r'reference/genres', ReferenceGenreViewSet, basename='reference-genre')
router.register(r'reference/tags', ReferenceTagViewSet, basename='reference-tag')
router.register(r'reference/playlists', ReferencePlaylistViewSet, basename='reference-playlist')
router.register(r'reference/manual-playlists', ReferenceManualPlaylistViewSet, basename='reference-manual-playlist')
router.register(r'reference/genre-playlists', ReferenceGenrePlaylistViewSet, basename='reference-genre-playlist')
router.register(r'reference/tag-playlists', ReferenceTagPlaylistViewSet, basename='reference-tag-playlist')
router.register(r'reference/plays', ReferencePlayViewSet, basename='reference-play')

router.register(r'me/library/uploaded', UploadedTrackViewSet, basename='me-uploaded-track')
router.register(r'me/artists', ArtistViewSet, basename='me-artist')
router.register(r'me/albums', AlbumViewSet, basename='me-album')
router.register(r'me/genres', GenreViewSet, basename='me-genre')
router.register(r'me/tags', TagViewSet, basename='me-tag')
router.register(r'me/playlists', PlaylistViewSet, basename='me-playlist')
router.register(r'me/manual-playlists', ManualPlaylistViewSet, basename='me-manual-playlist')
router.register(r'me/genre-playlists', GenrePlaylistViewSet, basename='me-genre-playlist')
router.register(r'me/tag-playlists', TagPlaylistViewSet, basename='me-tag-playlist')
router.register(r'me/plays', PlayViewSet, basename='me-play')

router.register(r'all-tracks', AllUploadedTracksViewSet, basename='all-uploaded-tracks')
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path(settings.API_ROOT_BASE, include(router.urls)),

    path('admin/', admin.site.urls),
    path('health/', HealthCheckView.as_view(), name='health-check'),

    path(settings.API_ROOT_BASE + 'auth/', include('django.contrib.auth.urls')),
    path(settings.API_ROOT_BASE + 'auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path(settings.API_ROOT_BASE + 'auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path(settings.API_ROOT_BASE + 'auth/spotify/', spotify_auth, name='api-auth-spotify'),


    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.STATIC_FILES_STATE in [StaticFileStates.COLLECTING, StaticFileStates.SERVING]:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
