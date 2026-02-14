import inspect
import pkgutil

from rest_framework import serializers

import api.serializer as serializer_package
from api.serializer.AppModelSerializer import AppModelSerializer
from api.test.utils.AppTestCase import AppTestCase


class TestModelSerializerInheritance(AppTestCase):
    """
    Test that all model serializers inherit from AppModelSerializer.

    AppModelSerializer maps DecimalField and GeneratedField (decimal output) to FloatField
    so API and OpenAPI schema use number instead of string, matching frontend types (e.g. Zod).
    """

    def _discover_model_serializer_classes(self):
        """
        Discover all model serializer classes in the api.serializer package.

        Returns:
            List of serializer classes that have Meta.model and subclass ModelSerializer.
        """
        serializer_classes = []
        serializer_package_path = list(serializer_package.__path__)

        for importer, modname, ispkg in pkgutil.walk_packages(
            path=serializer_package_path,
            prefix="api.serializer."
        ):
            if ispkg or modname.endswith(".Fields") or "test" in modname:
                continue

            try:
                module = __import__(modname, fromlist=[""])
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name == "AppModelSerializer":
                        continue
                    if obj.__module__ != modname:
                        continue
                    if not issubclass(obj, serializers.ModelSerializer):
                        continue
                    meta = getattr(obj, "Meta", None)
                    if meta is None or not getattr(meta, "model", None):
                        continue
                    serializer_classes.append(obj)
            except (ImportError, AttributeError, TypeError):
                continue

        return serializer_classes

    def test_all_model_serializers_inherit_from_app_model_serializer(self):
        """
        Verify that all model serializers inherit from AppModelSerializer.

        This ensures DecimalField and GeneratedField (decimal) are always serialized
        as JSON number, so OpenAPI schema and frontend types stay in sync.
        """
        serializer_classes = self._discover_model_serializer_classes()
        violations = []

        for serializer_class in serializer_classes:
            if AppModelSerializer not in serializer_class.__mro__:
                violations.append(
                    f"{serializer_class.__name__} ({serializer_class.__module__})"
                )

        assert not violations, (
            f"Found {len(violations)} model serializer(s) that do not inherit from AppModelSerializer:\n"
            + "\n".join(f"  - {v}" for v in violations)
            + "\n\nAll model serializers (Meta.model) must inherit from AppModelSerializer "
            "so decimal fields are serialized as number."
        )
