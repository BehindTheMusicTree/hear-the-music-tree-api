from rest_framework import serializers
from the_music_tree_genre_kit.serializer.model.criteria.output.simple import build_criteria_simple_serializer

from hear.model.criteria.Criteria import Criteria

from .CriteriaOutputFieldKey import CriteriaOutputFieldKey

_BaseCriteriaSimpleSerializer = build_criteria_simple_serializer(Criteria)


class CriteriaSimpleSerializer(_BaseCriteriaSimpleSerializer):
    # `side` lives only on the concrete `Genre` MTI subtype, not on the shared `Criteria`
    # table this serializer is built against -- this viewset/serializer is shared by both
    # `GenreViewSet` and `TagViewSet`, so read it defensively rather than assuming it's there.
    side = serializers.SerializerMethodField()

    def get_side(self, obj) -> str | None:
        return getattr(obj, CriteriaOutputFieldKey.SIDE.value, None)

    class Meta:
        model = Criteria
        fields = [
            CriteriaOutputFieldKey.UUID.value,
            CriteriaOutputFieldKey.NAME.value,
            CriteriaOutputFieldKey.PARENT.value,
            CriteriaOutputFieldKey.CREATED_ON.value,
            CriteriaOutputFieldKey.SIDE.value,
        ]
