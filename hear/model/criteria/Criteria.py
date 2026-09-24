from typing import TYPE_CHECKING

from django.db import models
from the_music_tree_genre_kit.criteria.AbstractCriteria import AbstractCriteria
from the_music_tree_genre_kit.track_mixin.TrackMixin import TrackMixin

from hear.model.criteria.CriteriaManager import CriteriaManager

from .Fields import Fields

if TYPE_CHECKING:
    from the_music_tree_genre_kit.track.Track import Track

    from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist


class Criteria(AbstractCriteria, TrackMixin):
    if TYPE_CHECKING:
        criteria_playlist: CriteriaPlaylist

    objects: CriteriaManager = CriteriaManager()

    @property
    def tracks(self) -> models.QuerySet[Track]:
        from hear.model.uploaded_track.UploadedTrack import UploadedTrack

        return UploadedTrack.objects.filter(genre=self)

    class Meta:
        db_table = "htmt_api_criteria"
        verbose_name = "Criteria"
        verbose_name_plural = "Criterias"
        constraints = [
            models.CheckConstraint(condition=~models.Q(_name=""), name="%(class)s_non_empty_name"),
            models.UniqueConstraint(fields=[Fields.USER, Fields.NAME_INTERNAL], name="unique_name_per_user"),
        ]
        indexes = [
            models.Index(fields=[Fields.USER, Fields.NAME_INTERNAL], name="%(class)s_user_name_idx"),
            models.Index(fields=[Fields.USER, Fields.UUID], name="%(class)s_user_uuid_idx"),
        ]
