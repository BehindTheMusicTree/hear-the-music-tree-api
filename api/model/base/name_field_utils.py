from typing import Any

from django.core.exceptions import FieldDoesNotExist
from django.db import models

from api.model.field.AppCharField import AppCharField

NAME_PUBLIC = "name"
NAME_INTERNAL = f"_{NAME_PUBLIC}"


def uses_internal_name(model: type[models.Model]) -> bool:
    try:
        field = model._meta.get_field(NAME_INTERNAL)
        return isinstance(field, AppCharField) and field.db_column == NAME_PUBLIC
    except FieldDoesNotExist:
        return False


def transform_name_fields(model: type[models.Model], **kwargs: Any) -> dict[str, Any]:
    """
    Transform name fields to internal name fields in all cases:
    - Direct field references (name → _name)
    - Relationship traversals (criteria__name → criteria___name)
    - Complex lookups (criteria__name__icontains → criteria___name__icontains)
    """
    transformed = {}

    for key, value in kwargs.items():
        # Handle direct name field references
        if key == NAME_PUBLIC and uses_internal_name(model):
            transformed[NAME_INTERNAL] = value
        # Handle relationship traversals and lookups containing __name
        elif "__" + NAME_PUBLIC in key:
            # Split on __name to preserve any lookups that come after
            parts = key.split("__" + NAME_PUBLIC)
            if len(parts) == 2:
                # parts[0] is the relationship path
                # parts[1] is either empty or contains lookups (like __icontains)
                transformed[parts[0] + "__" + NAME_INTERNAL + parts[1]] = value
            else:
                transformed[key] = value
        else:
            transformed[key] = value

    return transformed
