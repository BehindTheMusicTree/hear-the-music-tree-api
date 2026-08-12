from the_music_tree_genre_kit.serializer.model.criteria_lineage_rel.without_ascendant import (
    build_criteria_lineage_rel_without_ascendant_serializer,
)

from api.model.criteria.Criteria import Criteria
from api.model.criteria.lineage_rel.CriteriaLineageRel import CriteriaLineageRel

CriteriaLineageRelWithoutAscendantSerializer = build_criteria_lineage_rel_without_ascendant_serializer(
    CriteriaLineageRel, Criteria
)
