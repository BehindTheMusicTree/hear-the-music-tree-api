from typing import Any

from django.contrib.contenttypes.prefetch import GenericPrefetch
from rest_framework import serializers
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_genre_kit.playlist.Playlist import Playlist

from hear.model.play.Play import Play
from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from hear.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer
from hear.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from hear.serializer.model.uploaded_track.output.minimum import UploadedTrackMinimumSerializer

from .Fields import Fields


class PlayDetailedSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    content_type = AppCharField(source=f"{Fields.CONTENT_TYPE}.model")
    content = serializers.SerializerMethodField()

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):
        return queryset.select_related(f"{prefix}{Fields.CONTENT_TYPE}").prefetch_related(
            GenericPrefetch(
                f"{prefix}{Fields.CONTENT}",
                # A play's content type is the concrete playlist subtype, so each needs its own queryset.
                [
                    ManualPlaylist.objects.all(),
                    CriteriaPlaylistMinimumSerializer.setup_queryset(CriteriaPlaylist.objects.all()),
                    UploadedTrack.objects.prefetch_related("artists"),
                ],
            )
        )

    class Meta:
        model = Play
        fields = [Fields.UUID, Fields.CONTENT_TYPE, Fields.CONTENT, Fields.CREATED_ON]

    def get_content(self, obj: Play) -> dict[str, Any] | None:
        if obj.content is None:
            return None
        if isinstance(obj.content, Playlist):
            return PlaylistMinimumSerializer(obj.content).data
        if isinstance(obj.content, UploadedTrack):
            return UploadedTrackMinimumSerializer(obj.content).data
        raise NotImplementedError(f"No serializer for play content {type(obj.content).__name__}")
