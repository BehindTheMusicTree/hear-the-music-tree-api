from rest_framework.serializers import ModelSerializer
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer
from the_music_tree_genre_kit.serializer.field.foreign_key.DescendantAwareField import DescendantAwareField

from hear import settings
from hear.model.criteria.Criteria import Criteria
from hear.serializer.field.UniquePerUserNameField import UniquePerUserNameField

from .Fields import Fields


class CriteriaPostSerializer(ModelSerializer, AppInputSerializer):
    name = UniquePerUserNameField(
        max_length=settings.CRITERIA_NAME_LEN_MAX, allow_blank=False, required=True, model=Criteria
    )
    parent = DescendantAwareField(  # type: ignore
        queryset=Criteria.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Criteria
        fields = [Fields.NAME_PUBLIC, Fields.PARENT]
