from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from api.model.criteria.Criteria import Criteria
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer

from .CriteriaOutputFieldKey import CriteriaOutputFieldKey


class CriteriaSimpleSerializer(AppInputSerializer, serializers.ModelSerializer):
    parent = CriteriaMinimumSerializer()

    class Meta:
        model = Criteria
        fields = [
            CriteriaOutputFieldKey.UUID.value,
            CriteriaOutputFieldKey.NAME.value,
            CriteriaOutputFieldKey.PARENT.value,
            CriteriaOutputFieldKey.CREATED_ON.value,
        ]
