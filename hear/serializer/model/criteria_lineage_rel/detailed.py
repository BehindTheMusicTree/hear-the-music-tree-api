from the_music_tree_genre_kit.serializer.model.criteria_lineage_rel.detailed import (
    build_criteria_lineage_rel_detailed_serializer,
)

from hear.model.criteria.Criteria import Criteria
from hear.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel

CriteriaLineageRelDetailedSerializer = build_criteria_lineage_rel_detailed_serializer(CriteriaLineageRel, Criteria)
