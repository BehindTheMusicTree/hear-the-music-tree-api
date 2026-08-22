from typing import TYPE_CHECKING, Any, TypeVar

from the_music_tree_genre_kit.criteria.AbstractCriteriaManager import AbstractCriteriaManager

from .Fields import Fields

if TYPE_CHECKING:
    from hear.model.uploaded_track.UploadedTrack import UploadedTrack

    from .Criteria import Criteria

T = TypeVar("T", bound="Criteria")


class CriteriaManager(AbstractCriteriaManager[T]):
    model: type[T]

    def _create_lineage_rel(self, *, user: Any, descendant: T, ascendant: T, degree: int) -> None:
        from hear.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel

        CriteriaLineageRel.objects.create(user=user, descendant=descendant, ascendant=ascendant, degree=degree)

    def _on_created(self, instance: T) -> None:
        from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        CriteriaPlaylist.objects.create(user=instance.user, criteria=instance, type=instance.type)

    def _on_parent_changed(
        self, instance: T, *, old_parent: Criteria | None, old_root: Criteria, root_changed: bool
    ) -> None:
        from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        playlist_parent = instance.parent.criteria_playlist if instance.parent else None
        CriteriaPlaylist.objects.update_instance(
            instance=instance.criteria_playlist, **{Fields.PARENT: playlist_parent}
        )

        common_criteria = self.get_common_ascendant(instance, old_parent)
        CriteriaPlaylist.objects.update_ascendants_tracks(
            instance=instance.criteria_playlist, old_parent=old_parent, common_criteria=common_criteria
        )

        if root_changed:
            CriteriaPlaylist.objects.update_instance_and_children_root(
                instance=instance.criteria_playlist, root=instance.root.criteria_playlist
            )

    def _on_renamed(self, instance: T, *, old_name: str) -> None:
        if instance.uploaded_tracks:
            for uploaded_track in instance.uploaded_tracks.all():
                uploaded_track.update_file_metadata_from_uploaded_track_instance_values()

    def _on_track_genre_cleared(self, track: UploadedTrack) -> None:
        track.update_file_metadata_from_uploaded_track_instance_values()
