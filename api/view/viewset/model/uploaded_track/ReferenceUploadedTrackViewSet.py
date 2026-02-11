from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from api.view.viewset.model.uploaded_track.UploadedTrackViewSet import UploadedTrackViewSet


class ReferenceUploadedTrackViewSet(ReferenceViewSetMixin, UploadedTrackViewSet):
    permission_classes = [AllowAny]
