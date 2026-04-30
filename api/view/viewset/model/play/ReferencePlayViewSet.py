from rest_framework.permissions import AllowAny

from api.view.viewset.model.play.PlayViewSet import PlayViewSet
from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin


class ReferencePlayViewSet(ReferenceViewSetMixin, PlayViewSet):
    permission_classes = [AllowAny]
