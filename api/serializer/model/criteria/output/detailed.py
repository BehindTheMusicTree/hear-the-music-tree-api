from rest_framework import serializers
from rest_framework.fields import IntegerField
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField

from api.model.criteria.Criteria import Criteria
from api.model.criteria.Fields import Fields as ModelFields
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from api.serializer.model.criteria_lineage_rel.without_ascendant import CriteriaLineageRelWithoutAscendantSerializer
from api.serializer.model.criteria_lineage_rel.without_descendant import (
    CriteriaLineageRelWithoutDescendantSerializer,
)
from api.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from api.serializer.model.uploaded_track.output.simple.simple_without_album_and_genre import (
    UploadedTrackWithoutAlbumPlaylistGenreSerializer,
)

from .CriteriaOutputFieldKey import CriteriaOutputFieldKey


class CriteriaDetailedSerializer(AppInputSerializer, serializers.ModelSerializer):
    uploaded_tracks = UploadedTrackWithoutAlbumPlaylistGenreSerializer(
        source=CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL.value, many=True
    )
    uploaded_tracks_count = IntegerField(
        source=CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL.value
    )
    parent = CriteriaMinimumSerializer()
    ascendants = CriteriaLineageRelWithoutDescendantSerializer(source=ModelFields.ASCENDANTS_RELS, many=True)
    descendants = CriteriaLineageRelWithoutAscendantSerializer(source=ModelFields.DESCENDANTS_RELS, many=True)
    root = CriteriaMinimumSerializer()  # type: ignore
    children = CriteriaMinimumSerializer(many=True)
    criteria_playlist = CriteriaPlaylistMinimumSerializer()
    name = AppCharField(source=ModelFields.NAME_INTERNAL)

    class Meta:
        model = Criteria
        fields = [
            CriteriaOutputFieldKey.UUID.value,
            CriteriaOutputFieldKey.NAME.value,
            CriteriaOutputFieldKey.PARENT.value,
            CriteriaOutputFieldKey.ASCENDANTS.value,
            CriteriaOutputFieldKey.DESCENDANTS.value,
            CriteriaOutputFieldKey.ROOT.value,
            CriteriaOutputFieldKey.CHILDREN.value,
            CriteriaOutputFieldKey.CRITERIA_PLAYLIST.value,
            CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC.value,
            CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC.value,
            CriteriaOutputFieldKey.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC.value,
            CriteriaOutputFieldKey.CREATED_ON.value,
            CriteriaOutputFieldKey.UPDATED_ON.value,
        ]
