from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_genre_kit.serializer.model.criteria.output.side import CriteriaSideSerializerMixin

from hear.model.criteria.Criteria import Criteria
from hear.model.criteria.Fields import Fields as ModelFields

from .CriteriaOutputFieldKey import CriteriaOutputFieldKey


class CriteriaOverviewSerializer(CriteriaSideSerializerMixin, AppInputSerializer, serializers.ModelSerializer):
    uploaded_tracks_archived_count = serializers.IntegerField()
    name = AppCharField(source=ModelFields.NAME_INTERNAL)

    class Meta:
        model = Criteria
        fields = [
            CriteriaOutputFieldKey.UUID.value,
            CriteriaOutputFieldKey.NAME.value,
            CriteriaOutputFieldKey.SUMMARY.value,
            CriteriaOutputFieldKey.SIDE.value,
            CriteriaOutputFieldKey.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC.value,
        ]
