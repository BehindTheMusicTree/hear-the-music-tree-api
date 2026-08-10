from typing import TYPE_CHECKING, TypeVar

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models import QuerySet

from api.model.criteria.Fields import Fields as ModelFields
from api.model.criteria.type.CriteriaType import CriteriaType
from api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from api.model.uploaded_track_mixin.UploadedTrackMixinWithInternalNameManager import (
    UploadedTrackMixinWithInternalNameManager,
)
from api.serializer.model.criteria.input.Fields import Fields as InputFields
from api.serializer.model.criteria.input.tree_import.Fields import Fields as TreeImportFields

from .Fields import Fields

if TYPE_CHECKING:
    from api.model.user.User import User

    from .Criteria import Criteria

T = TypeVar("T", bound="Criteria")


class AbstractCriteriaManager(UploadedTrackMixinWithInternalNameManager[T]):
    """
    Owns the pure tree-structure logic for criteria (ascendant refresh, root
    propagation, common-ascendant lookup). Side effects outside the tree
    itself (playlists, file metadata, etc.) are left to subclasses via the
    `_on_created`/`_on_parent_changed`/`_on_renamed`/`_on_before_delete` hooks.
    """

    model: type[T]

    def _get_criteria_type(self) -> CriteriaType:
        from api.model.criteria.children.genre.Genre import Genre
        from api.model.criteria.children.tag.Tag import Tag

        type_pk: CriteriaTypePks
        if issubclass(self.model, Genre):
            type_pk = CriteriaTypePks.GENRE
        elif issubclass(self.model, Tag):
            type_pk = CriteriaTypePks.TAG
        else:
            raise ImproperlyConfigured(f"Invalid criteria type: {type(self.model)}")

        return CriteriaType(pk=type_pk)

    def _refresh_ascendants_of_instance(self, instance: T):
        from .lineage_rel.CriteriaLineageRel import CriteriaLineageRel

        instance.ascendants_rels.all().delete()
        current_degree = 1
        current_parent = instance.parent

        while current_parent:
            CriteriaLineageRel.objects.create(
                user=instance.user, descendant=instance, ascendant=current_parent, degree=current_degree
            )
            current_parent = current_parent.parent
            current_degree = current_degree + 1

    def _refresh_ascendants_of_instance_and_children(self, instance):
        self._refresh_ascendants_of_instance(instance)
        for child in self.filter(parent=instance):
            self._refresh_ascendants_of_instance_and_children(child)

    def _refresh_ascendants_of_descendants(self, instance):
        for child in instance.children.all():
            self._refresh_ascendants_of_instance_and_children(child)

    def get_default_ordering(self) -> list[str]:
        return [ModelFields.NAME_INTERNAL]

    def _on_created(self, instance: T) -> None:
        """Hook: react to a newly created criteria. No-op by default."""

    def _on_parent_changed(
        self, instance: T, *, old_parent: Criteria | None, old_root: Criteria, root_changed: bool
    ) -> None:
        """Hook: react to a criteria being reparented (and possibly re-rooted). No-op by default."""

    def _on_renamed(self, instance: T, *, old_name: str) -> None:
        """Hook: react to a criteria being renamed. No-op by default."""

    def _on_before_delete(self, instance: T) -> None:
        """Hook: react just before a criteria is deleted. No-op by default."""

    @transaction.atomic
    def create(self, **kwargs) -> T:
        criteria_type = self._get_criteria_type()
        instance: T = super().create(type=criteria_type, **kwargs)
        self._on_created(instance)
        self._refresh_ascendants_of_instance(instance)
        return instance

    @transaction.atomic
    def update_instance(self, instance: T, **kwargs) -> T:
        old_root = instance.root
        old_parent = instance.parent
        old_name = instance.name

        updated_instance: T = super().update_instance(instance, **kwargs)

        if old_parent != updated_instance.parent:
            self._refresh_ascendants_of_instance_and_children(updated_instance)

            root_changed = old_root != updated_instance.root
            if root_changed:
                self.update_children_root(criteria=updated_instance, new_root=updated_instance.root)

            self._on_parent_changed(
                updated_instance, old_parent=old_parent, old_root=old_root, root_changed=root_changed
            )

        if old_name != updated_instance.name:
            self._on_renamed(updated_instance, old_name=old_name)

        return updated_instance

    def get_common_ascendant(self, criteria_a: Criteria | None, criteria_b: Criteria | None) -> Criteria | None:
        if not criteria_a or not criteria_b:
            return None

        visited = set()
        current = criteria_a
        while current:
            visited.add(current)
            current = current.parent

        current = criteria_b
        while current:
            if current in visited:
                return current
            current = current.parent

        return None

    @transaction.atomic
    def delete_instance(self, instance: T) -> None:
        """
        Delete a criteria and handle tree relationships.

        When deleting a criteria:
        - If it has children and a parent, children are reassigned to the parent
        - If it has children but no parent, children become root criteria
        Non-tree side effects (uploaded tracks, playlists) are left to `_on_before_delete`.
        """
        if instance.children.exists():
            children = list(instance.children.all())

            for child in children:
                child.parent = instance.parent
                child.root = instance.parent or child
                child.save(update_fields=[Fields.PARENT, Fields.ROOT])
                self._refresh_ascendants_of_instance_and_children(child)
                self.update_children_root(child, child.root)

        # Model-level tree state must be updated before this hook runs: subclass hooks
        # (e.g. playlist maintenance) may re-derive fields from the criteria's current
        # parent/root, so they need the post-reassignment state, not the pre-delete one.
        self._on_before_delete(instance)

        # Delete the criteria instance directly
        # This will cascade delete its playlist due to foreign key relationships
        instance.delete()

    def get_roots(self, user: User) -> QuerySet[T]:
        return self.filter(user=user, parent__isnull=True)

    def update_children_root(self, criteria: Criteria, new_root: Criteria):
        children = criteria.children.all()
        if children.exists():
            children.update(root=new_root)
            for child in children:
                self.update_children_root(child, new_root)

    def build_criteria_tree(self, user: User) -> list[dict]:
        """
        Builds a tree structure of all criteria for a given user.
        The structure follows the format:
        {
          "name": "Criteria name",
          "children": [
            {
              "name": "Child criteria name",
              "children": []
            }
          ]
        }
        """
        # Get all criteria for the user
        queryset = self.filter(user=user).select_related(Fields.PARENT)

        # Build a dictionary of criteria by parent ID for efficient lookup
        criteria_by_parent = {}
        for criteria in queryset:
            # Handle both UUID and ID based parent references
            parent_id = criteria.parent.uuid if hasattr(criteria.parent, "uuid") else criteria.parent_id
            if parent_id not in criteria_by_parent:
                criteria_by_parent[parent_id] = []
            criteria_by_parent[parent_id].append(criteria)

        # Recursive function to build the tree
        def build_tree(parent_id):
            if parent_id not in criteria_by_parent:
                return []

            result = []
            for criteria in criteria_by_parent[parent_id]:
                # Get the appropriate ID for child references
                child_id = criteria.uuid if hasattr(criteria, "uuid") else criteria.id
                node = {InputFields.NAME_PUBLIC: criteria.name, InputFields.CHILDREN: build_tree(child_id)}
                result.append(node)

            return result

        # Start with root criteria (parent_id is None)
        return build_tree(None)

    @transaction.atomic
    def import_criteria_tree(self, user: User, data: dict) -> None:
        """
        Imports a tree structure of criteria, replacing all existing criteria.
        The input should be an array of criteria trees, where each tree follows the format:
        {
          "name": "Criteria name",
          "children": [
            {
              "name": "Child criteria name",
              "children": []
            }
          ]
        }
        """
        if not data:
            return

        # Delete all existing criteria for the user
        self.filter(user=user).delete()

        # Handle serializer.validated_data which will be a dict with a 'tree' key
        if isinstance(data, dict) and TreeImportFields.TREE in data:
            tree_data = data[TreeImportFields.TREE]
        elif isinstance(data, list):
            tree_data = data
        else:
            tree_data = []

        if not tree_data:
            return

        # Recursive function to create criteria and their children
        def create_criteria_tree(nodes, parent=None):
            for node in nodes:
                name = node.get(InputFields.NAME_PUBLIC)
                criteria = self.create(name=name, parent=parent, user=user)

                children = node.get("children", [])
                if children is None:
                    children = []

                if children:
                    create_criteria_tree(children, criteria)

        # Create all criteria trees
        create_criteria_tree(tree_data)
