import requests
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
from the_music_tree_api_kit.exception.validation.app.AppValidationException import AppValidationException
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

from api import settings


@deconstructible
class TrackUrlValidator(BaseValidator):
    def __init__(self, field_name="url", message=None):
        super().__init__(None, message)  # We don't use limit_value
        self.field_name = field_name

    def __call__(self, value):
        if not isinstance(value, str):
            raise AppValidationException(
                field_name=self.field_name,
                message="Invalid audio file URL",
                field_validation_error_code=FieldValidationErrorCode.URL_INVALID,
            )

        self._validate_url_format(value)
        self._validate_audio_extension(value)
        self._validate_remote_file_exists(value)

    def _validate_url_format(self, value: str):
        if not value.startswith("http"):
            raise AppValidationException(
                field_name=self.field_name,
                message="Invalid audio file URL",
                field_validation_error_code=FieldValidationErrorCode.URL_INVALID,
            )

    def _validate_audio_extension(self, value: str):
        if not any(value.lower().endswith(ext) for ext in settings.UPLOADED_TRACK_FILE_EXTENSIONS):
            raise AppValidationException(
                field_name=self.field_name,
                message="Invalid audio file extension",
                field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID,
            )

    def _validate_remote_file_exists(self, value: str):
        """HEAD/GET with Range to check reachability. Accept 200 or 206 (many servers return 200 for Range or after
        redirects).
        """
        try:
            response = requests.get(value, headers={"Range": "bytes=0-10"}, allow_redirects=True, timeout=10)
            if response.status_code not in (200, 206):
                raise AppValidationException(
                    field_name=self.field_name,
                    message="Invalid audio file URL",
                    field_validation_error_code=FieldValidationErrorCode.URL_NOT_FOUND,
                )
        except requests.RequestException:
            raise AppValidationException(
                field_name=self.field_name,
                message="Invalid audio file URL",
                field_validation_error_code=FieldValidationErrorCode.URL_NOT_FOUND,
            )
