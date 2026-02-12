from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from api.view.viewset.model.criteria.children.tag.TagViewSet import TagViewSet


class ReferenceTagViewSet(ReferenceViewSetMixin, TagViewSet):
    permission_classes = [AllowAny]
