from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from the_music_tree_api_kit.view.viewset.model.AppModelViewSet import AppModelViewSet

from api.filtering.set.play.PlayFilterSet import PlayFilterSet
from api.model.play.Play import Play
from api.serializer.model.play.input.schema.post import PlayPostSerializer
from api.serializer.model.play.output.detailed import PlayDetailedSerializer


class PlayViewSet(AppModelViewSet[Play]):
    def __init__(self, **kwargs):
        super().__init__(
            model_class=Play,
            filterset_class=PlayFilterSet,
            simple_serializer_class=PlayDetailedSerializer,
            detailed_serializer_class=PlayDetailedSerializer,
            create_serializer_class=PlayPostSerializer,
            **kwargs,
        )

    def list(self, *args, **kwargs) -> Response:
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    # @transaction.atomic not needed
    @extend_schema(request=PlayPostSerializer, responses=PlayDetailedSerializer)
    def create(self, request, *args, **kwargs):
        return self._handle_post(request)
