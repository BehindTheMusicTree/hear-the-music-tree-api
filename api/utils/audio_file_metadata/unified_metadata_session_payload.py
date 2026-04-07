"""Map metadata-session download JSON (validated by DRF) to audiometa unified-metadata patch keys."""

from typing import Any

from audiometa import UnifiedMetadataKey

from api.serializer.audio_metadata.Fields import Fields

_UNIFIED_IDS = frozenset(k.value for k in UnifiedMetadataKey)

_SESSION_ONLY_KEYS = frozenset({Fields.SESSION_TOKEN})


def build_unified_metadata_patch_from_validated_data(data: dict[str, Any]) -> dict[str, Any]:
    """Build a patch dict keyed by :class:`UnifiedMetadataKey` string values.

    Only keys in ``data`` that are valid unified metadata field ids are included (partial update).
    ``session_token`` is ignored.
    """
    out: dict[str, Any] = {}
    for key, value in data.items():
        if key in _SESSION_ONLY_KEYS:
            continue
        if key not in _UNIFIED_IDS:
            continue
        out[key] = value
    return out
