from audiometa import UnifiedMetadataKey

from api.serializer.audio_metadata.Fields import Fields
from api.utils.audio_file_metadata.unified_metadata_session_payload import (
    build_unified_metadata_patch_from_validated_data,
)


def test_empty_payload():
    assert build_unified_metadata_patch_from_validated_data({}) == {}


def test_legacy_keys_map_to_canonical():
    patch = build_unified_metadata_patch_from_validated_data(
        {
            Fields.ARTISTS_NAMES: ["A"],
            Fields.ALBUM_NAME: "Al",
            Fields.ALBUM_ARTISTS_NAMES: ["B"],
        }
    )
    assert patch == {
        UnifiedMetadataKey.ARTISTS.value: ["A"],
        UnifiedMetadataKey.ALBUM.value: "Al",
        UnifiedMetadataKey.ALBUM_ARTISTS.value: ["B"],
    }


def test_canonical_wins_over_legacy():
    patch = build_unified_metadata_patch_from_validated_data(
        {
            UnifiedMetadataKey.ARTISTS.value: ["Canon"],
            Fields.ARTISTS_NAMES: ["Legacy"],
        }
    )
    assert patch[UnifiedMetadataKey.ARTISTS.value] == ["Canon"]


def test_album_key_maps_for_programmatic_payload():
    patch = build_unified_metadata_patch_from_validated_data(
        {UnifiedMetadataKey.ALBUM.value: "Direct"}
    )
    assert patch == {UnifiedMetadataKey.ALBUM.value: "Direct"}


def test_artists_key_maps_for_programmatic_payload():
    patch = build_unified_metadata_patch_from_validated_data(
        {UnifiedMetadataKey.ARTISTS.value: ["A", "B"]}
    )
    assert patch == {UnifiedMetadataKey.ARTISTS.value: ["A", "B"]}


def test_album_artists_key_maps_for_programmatic_payload():
    patch = build_unified_metadata_patch_from_validated_data(
        {UnifiedMetadataKey.ALBUM_ARTISTS.value: ["AA"]}
    )
    assert patch == {UnifiedMetadataKey.ALBUM_ARTISTS.value: ["AA"]}


def test_unified_field_passthrough():
    patch = build_unified_metadata_patch_from_validated_data(
        {
            UnifiedMetadataKey.COMPOSERS.value: ["Mozart"],
            UnifiedMetadataKey.ISRC.value: "USRC17607839",
        }
    )
    assert patch == {
        UnifiedMetadataKey.COMPOSERS.value: ["Mozart"],
        UnifiedMetadataKey.ISRC.value: "USRC17607839",
    }
