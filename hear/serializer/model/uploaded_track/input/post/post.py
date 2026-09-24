import os
from typing import cast

from django.core.files.base import File as DjangoFile
from the_music_tree_api_kit.exception.validation.app.AppValidationException import AppValidationException
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from the_music_tree_api_kit.utils import data_transformer

from hear import settings
from hear.model.user.User import User
from hear.serializer.field.TrackFileField import TrackFileField
from hear.serializer.model.uploaded_track.input.input import UploadedTrackInputSerializer
from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.utils import audio_file_metadata, utils
from hear.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey
from hear.utils.audio_file_metadata.exceptions import FileCorruptedError


def _wire_key(key) -> str:
    return getattr(key, "value", key)


class UploadedTrackPostSerializer(UploadedTrackInputSerializer):
    file = TrackFileField(required=True)

    def _get_generated_title_from_data(self, file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).rsplit(".", 1)[0]
        filename = filename.rstrip()
        filename_without_expressions_to_exclude = data_transformer.remove_substrings_from_string(
            string_a=filename, substrings=settings.UPLOADED_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE
        )

        if len(filename_without_expressions_to_exclude) > settings.UPLOADED_TRACK_FILENAME_LEN_MAX:
            title = settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE + utils.generate_short_uu(
                settings.UPLOADED_TRACK_GENERATED_TITLE_LENGTH - len(settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE)
            )
        else:
            title = filename_without_expressions_to_exclude
        return title

    def _get_metadata_from_file(self, file) -> dict:
        try:
            return audio_file_metadata.get_app_metadata(
                file=file, normalized_rating_max_value=settings.UPLOADED_TRACK_RATING_VALUE_MAX
            )
        except FileCorruptedError as exc:
            raise AppValidationException(
                field_name=UploadedTrackInputFieldKey.TRACK_FILE_PUBLIC.value,
                message=str(exc),
                field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_CORRUPTED,
            )

    def _truncate_metadata_values(self, metadata_dict: dict) -> dict:
        metadata_str_max_lengths = {
            AppMetadataKey.TITLE: settings.UPLOADED_TRACK_TITLE_LEN_MAX,
            AppMetadataKey.ARTISTS_NAMES: settings.ARTISTS_NAMES_LEN_MAX,
            AppMetadataKey.ALBUM_NAME: settings.ALBUM_NAME_LEN_MAX,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: settings.ALBUM_ARTISTS_NAMES_FIELD_LEN_MAX,
            AppMetadataKey.GENRES_NAMES: settings.CRITERIA_NAME_LEN_MAX,
            AppMetadataKey.LANGUAGE: settings.LANGUAGE_LEN_MAX,
        }

        for key, max_length in metadata_str_max_lengths.items():
            metadata_value = cast(str, metadata_dict.get(key))
            if metadata_value:
                if key.get_optional_type() == list[str]:
                    truncated_values = []
                    for value in metadata_value:
                        truncated_values.append(value[:max_length])
                    metadata_dict[key] = truncated_values
                else:
                    metadata_dict[key] = metadata_value[:max_length]

        return metadata_dict

    def _extract_metadata_fields(self, metadata_dict: dict) -> dict:
        copy = data_transformer.get_copy_of_dict_including_only_specified_keys(
            data_dict=metadata_dict,
            keys=[AppMetadataKey.TITLE, AppMetadataKey.ARTISTS_NAMES, AppMetadataKey.RATING, AppMetadataKey.LANGUAGE],
        )
        data = {
            UploadedTrackInputFieldKey.TITLE.value: copy.get(AppMetadataKey.TITLE),
            UploadedTrackInputFieldKey.ARTISTS_NAMES.value: copy.get(AppMetadataKey.ARTISTS_NAMES),
            UploadedTrackInputFieldKey.RATING.value: copy.get(AppMetadataKey.RATING),
            UploadedTrackInputFieldKey.LANGUAGE.value: copy.get(AppMetadataKey.LANGUAGE),
        }
        if metadata_dict.get(AppMetadataKey.ALBUM_NAME) not in [None, ""]:
            data[UploadedTrackInputFieldKey.ALBUM_NAME.value] = metadata_dict.get(AppMetadataKey.ALBUM_NAME)
            data[UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value] = metadata_dict.get(
                AppMetadataKey.ALBUM_ARTISTS_NAMES, []
            )
        return data

    def _handle_genre(self, input_data: dict, file_metadata: dict, user: User):
        genres = file_metadata.get(AppMetadataKey.GENRES_NAMES) or []
        genre_name = genres[0] if genres else None
        if genre_name:
            from hear.model.criteria.children.genre.Genre import Genre

            input_data[UploadedTrackInputFieldKey.GENRE.value] = Genre.objects.get_or_create(
                user=user, name=genre_name
            )[0]

    def _get_input_data_from_file(self, file, user: User):
        file_metadata = self._get_metadata_from_file(file)
        file_metadata = self._truncate_metadata_values(file_metadata)

        input_data = self._extract_metadata_fields(file_metadata)
        self._handle_genre(user=user, input_data=input_data, file_metadata=file_metadata)

        input_data_clean = data_transformer.remove_none_or_empty_key_from_dict(input_data)
        input_data_clean[UploadedTrackInputFieldKey.TRACK_FILE_INTERNAL.value] = file

        return input_data_clean

    def validate(self, data: dict):
        self._validate_album_fields_from_data(data)

        user = self.context["request"].user
        file = cast(DjangoFile, data.get(UploadedTrackInputFieldKey.TRACK_FILE_PUBLIC.value))  # Required so not None
        input_data = self._get_input_data_from_file(file=file, user=user)

        keys = [
            UploadedTrackInputFieldKey.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE.value,
            UploadedTrackInputFieldKey.TITLE.value,
            UploadedTrackInputFieldKey.ARTISTS_NAMES.value,
            UploadedTrackInputFieldKey.ALBUM_NAME.value,
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value,
            UploadedTrackInputFieldKey.TRACK_NUMBER.value,
            UploadedTrackInputFieldKey.GENRE.value,
            UploadedTrackInputFieldKey.RATING.value,
            UploadedTrackInputFieldKey.LANGUAGE.value,
        ]
        data_transformer.override_dict1_with_dict2_values_for_each_key_in_dict2(dict1=input_data, dict2=data, keys=keys)

        if UploadedTrackInputFieldKey.ALBUM_NAME.value in data and data.get(
            UploadedTrackInputFieldKey.ALBUM_NAME.value
        ) in [None, ""]:
            input_data[UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES.value] = []
            input_data[UploadedTrackInputFieldKey.ALBUM_NAME.value] = ""
            input_data[UploadedTrackInputFieldKey.TRACK_NUMBER.value] = None

        self._validate_album_fields_from_data(input_data)

        input_data[UploadedTrackInputFieldKey.TRACK_FILE_INTERNAL.value] = data[
            UploadedTrackInputFieldKey.TRACK_FILE_PUBLIC.value
        ]

        if input_data.get(UploadedTrackInputFieldKey.TITLE.value) in [None, ""]:
            input_data[UploadedTrackInputFieldKey.TITLE.value] = self._get_generated_title_from_data(file, input_data)

        return super().validate(input_data)
