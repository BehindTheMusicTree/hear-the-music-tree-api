from drf_spectacular.utils import extend_schema  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework.response import Response  # type: ignore

from hear.model.criteria.children.genre.Genre import Genre
from hear.serializer.model.criteria.output.overview import CriteriaOverviewSerializer
from hear.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=Genre, **kwargs)

    @extend_schema(
        responses=CriteriaOverviewSerializer,
        description="Lightweight genre summary for detail panels, without tracks, lineage or playlist.",
    )
    @action(detail=True, methods=["get"])
    def overview(self, request: Request, *args, **kwargs) -> Response:
        return Response(data=CriteriaOverviewSerializer(self.get_object()).data)
