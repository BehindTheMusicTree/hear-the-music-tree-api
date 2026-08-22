from django.db import models
from the_music_tree_api_kit.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from the_music_tree_genre_kit.criteria.lineage_rel.AbstractCriteriaLineageRel import AbstractCriteriaLineageRel

from ..Criteria import Criteria
from ..Fields import Fields as CriteriaFields
from .Fields import Fields


class CriteriaLineageRel(AbstractCriteriaLineageRel):
    descendant = PrivateForeignKey(Criteria, on_delete=models.CASCADE, related_name=CriteriaFields.ASCENDANTS_RELS)
    ascendant = PrivateForeignKey(Criteria, on_delete=models.CASCADE, related_name=CriteriaFields.DESCENDANTS_RELS)

    def __str__(self):
        return f"Descendant {self.descendant.uuid} | Degree {self.degree} | Ascendant {self.ascendant.uuid}"

    class Meta:
        db_table = "htmt_api_criteria_lineage_rel"
        verbose_name = "Criteria Lineage Relation"
        verbose_name_plural = "Criteria Lineage Relations"
        indexes = [models.Index(fields=[Fields.USER], name="crit_lineage_rel_user_idx")]
