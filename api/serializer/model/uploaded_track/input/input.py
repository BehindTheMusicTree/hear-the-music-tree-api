from rest_framework import serializers
from the_music_tree_api_kit.exception.validation.app.AppValidationException import AppValidationException
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_api_kit.utils import data_transformer
from the_music_tree_genre_kit.serializer.field.criteria.CriteriaFieldInputType import CriteriaFieldInputType

from api import settings
from api.model.artist.Artist import Artist
from api.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as ModelFields
from api.model.user.User import User
from api.serializer.field.ArtistsNamesField import ArtistsNamesField
from api.serializer.field.criteria.GenreField import GenreField
from api.serializer.field.RatingField import RatingField
from api.serializer.field.TrackNumberField import TrackNumberField

from .UploadedTrackInputFieldKey import UploadedTrackInputFieldKey


def _wire_key(key) -> str:
    return getattr(key, "value", key)


class UploadedTrackInputSerializer(AppInputSerializer):
    track_file_fingerprint_must_be_unique = serializers.BooleanField(required=False)
    title = AppCharField(
        max_length=settings.UPLOADED_TRACK_TITLE_LEN_MAX, required=False, allow_blank=False, allow_null=True
    )
    force_title_generation = serializers.BooleanField(required=False)
    artists_names = ArtistsNamesField(max_length=settings.ARTISTS_NAMES_LEN_MAX, required=False, allow_null=True)
    album_name = AppCharField(max_length=settings.ALBUM_NAME_LEN_MAX, required=False, allow_blank=True, allow_null=True)
    album_artists_names = ArtistsNamesField(
        max_length=settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX, required=False, allow_null=True
    )
    track_number = TrackNumberField()
    genre = GenreField(
        input_types=[CriteriaFieldInputType.UUID, CriteriaFieldInputType.NAME], required=False, allow_null=True
    )
    rating = RatingField()
    language = AppCharField(max_length=settings.LANGUAGE_LEN_MAX, required=False, allow_blank=True, allow_null=True)

    def _update_model_data_with_album_if_name(self, user: User, data: dict):
        if not (
            UploadedTrackInputFieldKey.ALBUM_NAME.value in data
            or UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value in data
            or UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value in data
        ):
            return
        from api.model.album.Album import Album

        album_name = data.pop(UploadedTrackInputFieldKey.ALBUM_NAME.value, None)
        album_artists_names = (
            data.pop(UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value, None)
            or data.pop(UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value, None)
            or []
        )
        if album_name is not None:
            if album_name == "":
                data[ModelFields.ALBUM.value] = None
            else:
                album = Album.objects.get_album_from_name_and_album_artists_names_after_potential_creations(
                    user=user, name=album_name, album_artists_names=album_artists_names
                )
                data[ModelFields.ALBUM.value] = album
        elif not album_artists_names:
            data[ModelFields.ALBUM.value] = None

    def _update_data_with_artists_if_names_otherwise_empty_list(self, user: User, data: dict) -> None:
        if UploadedTrackInputFieldKey.ARTISTS_NAMES.value in data:
            artists_names = data.pop(UploadedTrackInputFieldKey.ARTISTS_NAMES.value) or []
            artists = Artist.objects.get_artists_list_from_names_after_potential_creation(
                user=user, artists_names=artists_names
            )
            data[ModelFields.ARTISTS.value] = artists

    def _validate_album_fields_from_data(self, data: dict):
        album_artists_provided = (
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value in data
            or UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value in data
        )
        if album_artists_provided and UploadedTrackInputFieldKey.ALBUM_NAME.value not in data:
            raise AppValidationException(
                message="Album name is required when album artists field is provided",
                field_name=UploadedTrackInputFieldKey.ALBUM_NAME.value,
                field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING,
            )
        if UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value in data:
            album_artists_val = data.get(UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value)
            if album_artists_val not in (None, []) and data.get(UploadedTrackInputFieldKey.ALBUM_NAME.value) in (
                None,
                "",
            ):
                raise AppValidationException(
                    message="Album name is required when album artists field is provided",
                    field_name=UploadedTrackInputFieldKey.ALBUM_NAME.value,
                    field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING,
                )
        if UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value in data:
            album_artists_val = data.get(UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value)
            if album_artists_val not in (None, []) and data.get(UploadedTrackInputFieldKey.ALBUM_NAME.value) in (
                None,
                "",
            ):
                raise AppValidationException(
                    message="Album name is required when album artists field is provided",
                    field_name=UploadedTrackInputFieldKey.ALBUM_NAME.value,
                    field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING,
                )

        if UploadedTrackInputFieldKey.TRACK_NUMBER.value in data:
            if data.get(UploadedTrackInputFieldKey.TRACK_NUMBER.value) not in [None, ""] and data.get(
                UploadedTrackInputFieldKey.ALBUM_NAME.value
            ) in [None, ""]:
                raise AppValidationException(
                    field_name=UploadedTrackInputFieldKey.ALBUM_NAME.value,
                    message="Album name must be specified if track position is.",
                    field_validation_error_code=FieldValidationErrorCode.DEPENDENCY_MISSING,
                )

    def validate(
        self,
        data: dict,
    ):
        lang_key = UploadedTrackInputFieldKey.LANGUAGE.value
        if lang_key in data and data[lang_key] == "":
            data[lang_key] = None
        data_transformer.update_dict_converting_str_to_int_value_if_set(key=ModelFields.RATING.value, data=data)

        user = self.context["request"].user
        data[ModelFields.USER.value] = user

        self._update_data_with_artists_if_names_otherwise_empty_list(user=user, data=data)
        self._update_model_data_with_album_if_name(user=user, data=data)

        return super().validate(data)
