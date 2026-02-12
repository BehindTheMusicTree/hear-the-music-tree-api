from api.model.user.User import User


class ReferenceViewSetMixin:
    """Use for reference (public) endpoints so the queryset is always scoped to the system user."""

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        request.user = User.objects.get_system_user()
