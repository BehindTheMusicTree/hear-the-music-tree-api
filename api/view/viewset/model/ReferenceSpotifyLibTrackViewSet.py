from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from api.view.viewset.model.SpotifyLibTrackViewSet import SpotifyLibTrackViewSet


class ReferenceSpotifyLibTrackViewSet(ReferenceViewSetMixin, SpotifyLibTrackViewSet):
    permission_classes = [AllowAny]
