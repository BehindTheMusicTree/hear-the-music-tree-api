from django_filters.filterset import FilterSet
from the_music_tree_api_kit.base.BaseQuerySet import BaseQuerySet

from hear.filtering.filter.char.EnumCharFilter import EnumCharFilter


class OptionalEnumCharFilter(EnumCharFilter):
    parent: FilterSet

    def filter(self, qs: BaseQuerySet, value: str) -> BaseQuerySet:
        parent_data = getattr(self.parent, "data", {})

        if (self.field_name_public or self.field_name) not in parent_data:
            return qs

        return super().filter(qs, value)
