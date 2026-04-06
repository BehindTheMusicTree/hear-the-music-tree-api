"""Map metadata-session download JSON (validated by DRF) to audiometa unified-metadata patch keys."""

from typing import Any

from audiometa import UnifiedMetadataKey

_LEGACY_TO_CANONICAL_LIST = (
    ("artists_names", "artists"),
    ("album_name", "album"),
    ("album_artists_names", "album_artists"),
)

_UNIFIED_IDS = frozenset(k.value for k in UnifiedMetadataKey)

_SKIP_KEYS = frozenset(
    {
        "session_token",
        "artists",
        "artists_names",
        "album",
        "album_name",
        "album_artists",
        "album_artists_names",
    }
)


def build_unified_metadata_patch_from_validated_data(data: dict[str, Any]) -> dict[str, Any]:
    """Build a patch dict keyed by :class:`UnifiedMetadataKey` string values.

    ``artists_names``, ``album_name``, and ``album_artists_names`` map to unified ``artists``,
    ``album``, and ``album_artists``. If both legacy and unified keys appear for the same
    logical field (e.g. ``artists_names`` and ``artists``), the unified key wins. Raw unified
    keys may still appear in ``data`` from programmatic callers. Only keys present in ``data``
    are included (partial update).
    """
    out: dict[str, Any] = {}

    for legacy, canonical in _LEGACY_TO_CANONICAL_LIST:
        if canonical in data:
            out[canonical] = data[canonical]
        elif legacy in data:
            out[canonical] = data[legacy]

    for key, value in data.items():
        if key in _SKIP_KEYS:
            continue
        if key not in _UNIFIED_IDS:
            continue
        out[key] = value

    return out
