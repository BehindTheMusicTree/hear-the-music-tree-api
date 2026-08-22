from rest_framework import serializers

from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from hear.serializer.model.playlist.children.criteria.output.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class CriteriaPlaylistMinimumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID, Fields.NAME]
