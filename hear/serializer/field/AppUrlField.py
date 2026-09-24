from typing import Any

from rest_framework import serializers
from the_music_tree_api_kit.serializer.field.AppField import AppField


class AppUrlField(AppField, serializers.URLField):
    """Custom CharField used to extend AppField so that fail() calls are converted into AppValidationExceptions."""

    def to_internal_value(self, data: Any) -> str:
        return serializers.URLField.to_internal_value(self, data)
