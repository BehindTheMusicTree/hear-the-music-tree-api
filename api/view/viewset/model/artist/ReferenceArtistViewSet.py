from rest_framework.permissions import AllowAny

from api.view.viewset.model.artist.ArtistViewSet import ArtistViewSet
from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin


class ReferenceArtistViewSet(ReferenceViewSetMixin, ArtistViewSet):
    permission_classes = [AllowAny]
