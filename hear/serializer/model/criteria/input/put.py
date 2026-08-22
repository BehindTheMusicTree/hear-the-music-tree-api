from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_api_kit.serializer.PutSerializer import PutSerializer
from the_music_tree_genre_kit.serializer.field.foreign_key.DescendantAwareField import DescendantAwareField

from hear import settings
from hear.model.criteria.Criteria import Criteria

from .Fields import Fields


class CriteriaPutSerializer(PutSerializer):
    name = AppCharField(max_length=settings.CRITERIA_NAME_LEN_MAX, required=False)
    parent: DescendantAwareField = DescendantAwareField(
        queryset=Criteria.objects.all(),  # type: ignore
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
