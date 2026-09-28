from rest_framework import serializers
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin
from the_music_tree_genre_kit.playlist.Fields import Fields as PlaylistModelFields
from the_music_tree_genre_kit.playlist.Playlist import Playlist

from hear.serializer.model.playlist.base.output.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME


class PlaylistMinimumSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    @classmethod
    def setup_queryset(cls, queryset, prefix=""):
        # Playlist.name and type_label resolve through the subtype, one query per row otherwise.
        criteria_playlist = f"{prefix}{PlaylistModelFields.CRITERIA_PLAYLIST}"
        return queryset.select_related(
            f"{prefix}{PlaylistModelFields.MANUAL_PLAYLIST}",
            f"{criteria_playlist}__criteria",
            f"{criteria_playlist}__type",
        )

    class Meta:
        model = Playlist
        fields = [Fields.UUID, Fields.NAME]
