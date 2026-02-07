from rest_framework.permissions import AllowAny

from api.model.user.User import User
from api.view.viewset.model.UploadedTrackViewSet import UploadedTrackViewSet


class ReferenceUploadedTrackViewSet(UploadedTrackViewSet):
    permission_classes = [AllowAny]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.is_authenticated:
            request.user = User.objects.get_system_user()
