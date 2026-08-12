from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from api.model.criteria.Criteria import Criteria

from .CriteriaOutputFieldKey import CriteriaOutputFieldKey


class CriteriaMinimumSerializer(AppInputSerializer, serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = [CriteriaOutputFieldKey.UUID.value, CriteriaOutputFieldKey.NAME.value]
