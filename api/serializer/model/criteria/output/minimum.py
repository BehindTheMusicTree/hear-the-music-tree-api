from rest_framework import serializers

from api.model.criteria.Criteria import Criteria
from api.serializer.AppInputSerializer import AppInputSerializer

from .CriteriaOutputFieldKey import CriteriaOutputFieldKey


class CriteriaMinimumSerializer(AppInputSerializer, serializers.ModelSerializer):

    class Meta:
        model = Criteria
        fields = [
            CriteriaOutputFieldKey.UUID.value,
            CriteriaOutputFieldKey.NAME.value,
        ]
