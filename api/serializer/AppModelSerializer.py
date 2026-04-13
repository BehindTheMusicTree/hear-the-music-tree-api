from django.core.exceptions import FieldDoesNotExist
from django.db import models
from rest_framework import serializers

_FLOAT_FIELD_EXCLUDED_KWARGS = frozenset({"max_digits", "decimal_places", "model_field"})


def _float_field_kwargs(field_kwargs: dict) -> dict:
    return {k: v for k, v in field_kwargs.items() if k not in _FLOAT_FIELD_EXCLUDED_KWARGS}


class AppModelSerializer(serializers.ModelSerializer):
    """
    ModelSerializer that serializes DecimalField as JSON number (float) instead of string.

    - serializer_field_mapping: model DecimalField -> FloatField.
    - build_field: GeneratedField with output_field DecimalField -> FloatField so
      size_in_ko / size_in_mo etc. are serialized as number without explicit field.
    """

    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        models.DecimalField: serializers.FloatField,
    }

    def build_field(self, field_name, info, model_class, nested_depth):
        field_cls, field_kwargs = super().build_field(field_name, info, model_class, nested_depth)
        if field_cls is serializers.FloatField:
            field_kwargs = _float_field_kwargs(field_kwargs)
        try:
            model_field = model_class._meta.get_field(field_name)
        except FieldDoesNotExist:
            return (field_cls, field_kwargs)
        generated_field_cls = getattr(models, "GeneratedField", None)
        if generated_field_cls is not None and isinstance(model_field, generated_field_cls):
            if isinstance(model_field.output_field, models.DecimalField):
                return (serializers.FloatField, _float_field_kwargs(field_kwargs))
        return (field_cls, field_kwargs)
