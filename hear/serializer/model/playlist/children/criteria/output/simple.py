from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from hear.serializer.model.criteria.output.simple import CriteriaSimpleSerializer
from hear.serializer.model.playlist.base.output.UploadedTracksCountsMixin import UploadedTracksCountsMixin
from hear.serializer.model.playlist.children.criteria.output.Fields import Fields as AvailableFields
from hear.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    CRITERIA = AvailableFields.CRITERIA
    PARENT = AvailableFields.PARENT
    ROOT = AvailableFields.ROOT
    CREATED_ON = AvailableFields.CREATED_ON
    UPDATED_ON = AvailableFields.UPDATED_ON


class CriteriaPlaylistSimpleSerializer(UploadedTracksCountsMixin, serializers.ModelSerializer):
    criteria = CriteriaSimpleSerializer()
    parent = CriteriaPlaylistMinimumSerializer()
    root = CriteriaPlaylistMinimumSerializer()  # type: ignore
    uploaded_tracks_count = serializers.SerializerMethodField()

    def to_representation(self, instance):
        if not isinstance(instance, CriteriaPlaylist):
            raise ImproperlyConfigured("Invalid instance type")
        return super().to_representation(instance)

    class Meta:
        model = CriteriaPlaylist
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.CRITERIA,
            Fields.PARENT,
            Fields.ROOT,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
        ]
