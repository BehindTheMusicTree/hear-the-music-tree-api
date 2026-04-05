from api.utils.audio_file_metadata.unified_metadata_session_payload import (
    build_unified_metadata_patch_from_validated_data,
)


def test_empty_payload():
    assert build_unified_metadata_patch_from_validated_data({}) == {}


def test_legacy_keys_map_to_canonical():
    patch = build_unified_metadata_patch_from_validated_data(
        {"artists_names": ["A"], "album_name": "Al", "album_artists_names": ["B"]}
    )
    assert patch == {"artists": ["A"], "album": "Al", "album_artists": ["B"]}


def test_canonical_wins_over_legacy():
    patch = build_unified_metadata_patch_from_validated_data(
        {"artists": ["Canon"], "artists_names": ["Legacy"]}
    )
    assert patch["artists"] == ["Canon"]


def test_unified_field_passthrough():
    patch = build_unified_metadata_patch_from_validated_data({"composer": ["Mozart"], "isrc": "USRC17607839"})
    assert patch == {"composer": ["Mozart"], "isrc": "USRC17607839"}
