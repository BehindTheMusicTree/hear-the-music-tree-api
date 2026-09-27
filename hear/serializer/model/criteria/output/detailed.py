from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_genre_kit.serializer.model.criteria.output.side import CriteriaSideSerializerMixin

from hear.model.criteria.Criteria import Criteria
from hear.model.criteria.Fields import Fields as ModelFields
from hear.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from hear.serializer.model.criteria_lineage_rel.without_ascendant import CriteriaLineageRelWithoutAscendantSerializer
from hear.serializer.model.criteria_lineage_rel.without_descendant import (
    CriteriaLineageRelWithoutDescendantSerializer,
)
from hear.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from hear.serializer.model.uploaded_track.output.simple.simple_without_album_and_genre import (
    UploadedTrackWithoutAlbumPlaylistGenreSerializer,
)

from .CriteriaOutputFieldKey import CriteriaOutputFieldKey


class CriteriaDetailedSerializer(CriteriaSideSerializerMixin, AppInputSerializer, serializers.ModelSerializer):
    uploaded_tracks = UploadedTrackWithoutAlbumPlaylistGenreSerializer(source="uploaded_tracks_not_archived", many=True)
    uploaded_tracks_count = serializers.IntegerField(source="uploaded_tracks_not_archived_count")
    uploaded_tracks_archived_count = serializers.IntegerField()
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
            CriteriaOutputFieldKey.SIDE.value,
            CriteriaOutputFieldKey.ROOT.value,
            CriteriaOutputFieldKey.CHILDREN.value,
            CriteriaOutputFieldKey.CRITERIA_PLAYLIST.value,
            CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC.value,
            CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC.value,
            CriteriaOutputFieldKey.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC.value,
            CriteriaOutputFieldKey.CREATED_ON.value,
            CriteriaOutputFieldKey.UPDATED_ON.value,
        ]
