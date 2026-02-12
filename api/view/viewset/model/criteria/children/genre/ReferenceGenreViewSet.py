from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from api.view.viewset.model.criteria.children.genre.GenreViewSet import GenreViewSet


class ReferenceGenreViewSet(ReferenceViewSetMixin, GenreViewSet):
    permission_classes = [AllowAny]
