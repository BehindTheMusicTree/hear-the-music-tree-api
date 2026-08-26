from the_music_tree_genre_kit.serializer.model.criteria.output.CriteriaOutputFieldKey import (
    CriteriaOutputFieldKey as KitCriteriaOutputFieldKey,
)

from hear.serializer.model.criteria.output.CriteriaOutputFieldKey import CriteriaOutputFieldKey
from hear.test.utils.AppTestCase import AppTestCase


class TestCriteriaOutputFieldKey(AppTestCase):
    """
    Guard against hear's CriteriaOutputFieldKey silently drifting from the kit's base enum.

    hear's enum hand-copies the kit's base members instead of inheriting them (StrEnum can't
    be subclassed once it has members), so a field added to the kit's enum has no mechanism
    to propagate here automatically. This test fails as soon as that happens, instead of the
    field silently missing from API output.
    """

    def test_all_kit_members_are_mirrored_with_the_same_value(self):
        missing = []
        mismatched = []

        for kit_member in KitCriteriaOutputFieldKey:
            local_member = getattr(CriteriaOutputFieldKey, kit_member.name, None)
            if local_member is None:
                missing.append(kit_member.name)
            elif local_member.value != kit_member.value:
                mismatched.append(f"{kit_member.name}: kit={kit_member.value!r} local={local_member.value!r}")

        assert not missing, (
            f"CriteriaOutputFieldKey is missing member(s) present in the kit's base enum: {missing}. "
            "Add them to hear/serializer/model/criteria/output/CriteriaOutputFieldKey.py "
            "(and wire them into the relevant serializer's Meta.fields if the field should be exposed)."
        )
        assert not mismatched, f"CriteriaOutputFieldKey member value(s) diverge from the kit's base enum: {mismatched}"
