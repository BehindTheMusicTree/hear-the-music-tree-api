from rest_framework.permissions import AllowAny

from api.view.viewset.model.criteria.children.tag.TagViewSet import TagViewSet
from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin


class ReferenceTagViewSet(ReferenceViewSetMixin, TagViewSet):
    permission_classes = [AllowAny]
