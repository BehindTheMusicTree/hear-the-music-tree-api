"""
Custom OpenAPI schema inspector for drf-spectacular.

Extends AutoSchema to correctly map Django model fields that drf-spectacular does
not handle out of the box:

- **GeneratedField** (Django 5+): Recurses into ``output_field`` so the schema
  reflects the actual type (e.g. DecimalField) instead of failing or defaulting
  to string.
- **DecimalField** in fallback path: When the inspector falls back to
  ``serializer_field_mapping`` (e.g. for GeneratedField with decimal output),
  it instantiates ``DecimalField`` with ``max_digits`` and ``decimal_places``
  from the model field instead of calling ``DecimalField()`` with no arguments,
  which would raise TypeError.

Used as ``DEFAULT_SCHEMA_CLASS`` in REST_FRAMEWORK settings so /schema/ and
/docs/ endpoints work with models that use GeneratedField or DecimalField.
"""

from django.db import models
from drf_spectacular.drainage import error, warn
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_basic_type, get_manager
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info


class AppAutoSchema(AutoSchema):
    """
    Drf-spectacular AutoSchema that supports GeneratedField and DecimalField.

    Overrides _map_model_field to avoid TypeError when generating the OpenAPI
    schema for serializers whose models use Django GeneratedField (e.g. computed
    columns) or DecimalField where the default mapping would instantiate
    DecimalField without required kwargs.
    """

    def _map_model_field(self, model_field, direction):
        """Map a Django model field to an OpenAPI schema, with GeneratedField and DecimalField fixes."""
        if not isinstance(model_field, models.Field):
            raise TypeError(f"model_field must be a django.db.models.Field, got {type(model_field).__name__!r}")

        generated_field_cls = getattr(models, "GeneratedField", None)
        if generated_field_cls is not None and isinstance(model_field, generated_field_cls):
            return self._map_model_field(model_field.output_field, direction)

        try:
            field_cls, field_kwargs = serializers.ModelSerializer().build_field(
                field_name=model_field.name,
                info=get_field_info(model_field.model),
                model_class=model_field.model,
                nested_depth=0,
            )
            field = field_cls(**field_kwargs)
            field.field_name = model_field.name
        except Exception:
            field = None

        if field and isinstance(field, serializers.PrimaryKeyRelatedField):
            if not field.queryset:
                field.queryset = get_manager(model_field.related_model).none()
            return self._map_serializer_field(field, direction)
        if isinstance(field, serializers.ManyRelatedField):
            if not field.child_relation.queryset:
                field.child_relation.queryset = get_manager(model_field.related_model).none()
            return self._map_serializer_field(field, direction)
        if field and not isinstance(field, (serializers.ReadOnlyField, serializers.ModelField)):
            return self._map_serializer_field(field, direction)
        if isinstance(model_field, models.ForeignKey):
            return self._map_model_field(model_field.target_field, direction)
        if hasattr(models, "JSONField") and isinstance(model_field, models.JSONField):
            return build_basic_type(OpenApiTypes.ANY)
        if isinstance(model_field, models.BinaryField):
            return build_basic_type(OpenApiTypes.BYTE)
        if hasattr(models, model_field.get_internal_type()):
            internal_type = getattr(models, model_field.get_internal_type())
            field_cls = serializers.ModelSerializer.serializer_field_mapping.get(internal_type)
            if not field_cls:
                warn(
                    f'model field "{model_field.get_internal_type()}" has no mapping in '
                    f'ModelSerializer. It may be a deprecated field. Defaulting to "string"'
                )
                return build_basic_type(OpenApiTypes.STR)
            if field_cls is serializers.DecimalField:
                effective = getattr(model_field, "output_field", model_field)
                if hasattr(effective, "max_digits") and hasattr(effective, "decimal_places"):
                    serializer_field = field_cls(
                        max_digits=effective.max_digits, decimal_places=effective.decimal_places
                    )
                else:
                    serializer_field = field_cls(max_digits=5, decimal_places=2)
            else:
                serializer_field = field_cls()
            return self._map_serializer_field(serializer_field, direction)
        error(
            f'could not resolve model field "{model_field}". Failed to resolve through '
            f"serializer_field_mapping, get_internal_type(), or any override mechanism. "
            f'Defaulting to "string"'
        )
        return build_basic_type(OpenApiTypes.STR)
