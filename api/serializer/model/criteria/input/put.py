from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_api_kit.serializer.PutSerializer import PutSerializer

from api import settings
from api.model.criteria.Criteria import Criteria
from api.serializer.field.foreign_key.DescendantAwareField import DescendantAwareField

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
