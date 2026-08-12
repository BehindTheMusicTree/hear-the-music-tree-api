from the_music_tree_genre_kit.serializer.model.criteria_lineage_rel.without_descendant import (
    build_criteria_lineage_rel_without_descendant_serializer,
)

from api.model.criteria.Criteria import Criteria
from api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel

CriteriaLineageRelWithoutDescendantSerializer = build_criteria_lineage_rel_without_descendant_serializer(
    CriteriaLineageRel, Criteria
)
