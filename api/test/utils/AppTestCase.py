from pathlib import Path
from typing import Generic, Type, TypeVar, Union, cast
import os
from uuid import UUID

from django.contrib.auth.hashers import make_password
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from api import settings
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.model.user.User import User
from api.model.uuid.Fields import Fields as UuidModelFields
from api.serializer.model.uploaded_track.input.post.Fields import Fields as UploadedTrackPostFields
from api.test.utils.AppApiClient import AppApiClient
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.utils.ModelFixtureFactory import ModelFixtureFactory
from api.utils import audio_file_metadata, data_transformer
from api.view.error.ErrorResponseFields import ErrorResponseFields
from api.view.pagination.PaginatedResponseFields import PaginatedResponseFields


T = TypeVar('T', bound=models.Model)


class AppTestCase(TestCase, Generic[T]):
    model_class: Type[T]  # Must be defined in child classes
    saved_object: T  # Must be defined in child classes
    is_from_uploaded_track_test_case: bool = False

    api_client: AppApiClient
    saved_uploaded_track_metadata_with_raw_rating: dict

    TEST_FILES_BASE_DIR = Path(__file__).parent.parent / 'utils' / 'uploaded_track' / 'files'

    def _login_as_user(self, user: User):
        self.api_client.force_authenticate(user=user)
        token = AccessToken.for_user(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def _login_as_test_user1(self):
        self._login_as_user(self.test_user1)

    def _login_as_test_user2(self):
        self._login_as_user(self.test_user2)

    def _login_as_spotify_test_user_1(self):
        self._login_as_user(self.spotify_test_user_1)

    def _login_as_spotify_test_user_2(self):
        self._login_as_user(self.spotify_test_user_2)

    def _login_as_test_admin(self):
        self._login_as_user(self.test_admin_user)

    def _logout(self):
        self.api_client.force_authenticate(user=None)

    def _set_saved_object_from_response(self, response):
        if not hasattr(self, 'model_class') or self.model_class is None:
            raise NotImplementedError("Test case must define model_class")

        uuid = response.json()[UuidModelFields.UUID]
        # At this point model_class is guaranteed to be a Model class with objects manager
        self.saved_object = self.model_class.objects.get(uuid=uuid)  # type: ignore
        if isinstance(self.saved_object, UploadedTrack):
            self._set_saved_uploaded_track_metadata()

    def _set_single_result(self, response):
        self.result = response.json()
        if hasattr(self, 'model_class'):
            self._set_saved_object_from_response(response)
        else:
            raise NotImplementedError("Test case must define model_class")

    def _set_results_without_model_class(self, response):
        if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            self._set_results_attributes(response)
        else:
            self._set_error_response_result_if_failure(response)

    def _set_results(self, response):
        if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            if response.status_code is not status.HTTP_204_NO_CONTENT:
                # list endpoints return paginated results
                if isinstance(response.json(), dict) and PaginatedResponseFields.RESULTS in response.json():
                    self._set_results_attributes(response)
                else:
                    self._set_single_result(response)
        else:
            self._set_error_response_result_if_failure(response)

    def _set_error_response_result_if_failure(self, response):
        """
        Handles responses with field errors in the format:
        {
            "code": 2001,
            "message": "Bad Request",
            "success": false,
            "details": [{
                "message": "One or more fields contain invalid data. Please check the error details for specific 
                    validation requirements",
                "fieldErrors": {
                    "field1": {"message": "...", "code": "..."},
                    "field2": {"message": "...", "code": "..."}
                }
            }]
        }
        """
        if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            return

        self.bad_request_result = response.json()
        bad_request_result_details = self.bad_request_result.get(ErrorResponseFields.DETAILS, {})
        self.bad_request_result_field_errors_json = bad_request_result_details.get(
            ErrorResponseFields.FIELD_ERRORS) if isinstance(
            bad_request_result_details, dict) else None
        if self.bad_request_result_field_errors_json:
            # Convert field errors to a list format for easier testing
            self.bad_request_result_field_errors = []
            for field_name, error_list in self.bad_request_result_field_errors_json.items():
                # error_list is a list of error dictionaries
                for error in error_list:
                    self.bad_request_result_field_errors.append({
                        'field': field_name,
                        'message': error['message'],
                        'code': error['code']
                    })

    def _set_results_attributes(self, response):
        response_json = response.json()
        self.results = response_json[PaginatedResponseFields.RESULTS]
        self.results_overall_total = response_json[PaginatedResponseFields.OVERALL_TOTAL]

    def _set_saved_uploaded_track_metadata(self):
        saved_uploaded_track = cast(UploadedTrack, self.saved_object)
        self.saved_uploaded_track_metadata_with_raw_rating = audio_file_metadata.get_app_metadata(
            file=saved_uploaded_track.track_file.file)

    # Defined here and not in UploadedTrackTestCase because other views needs sometimes to post a track for testing purposes
    # (testing metadata updates for example)
    def _post_uploaded_track(self, test_uploaded_track_filename: UploadedTrackTestFilename = UploadedTrackTestFilename.DEFAULT_MP3,
                             **kwargs) -> Union[JsonResponse, HttpResponse]:
        file_abs_path = self.TEST_FILES_BASE_DIR / test_uploaded_track_filename.value

        self._used_upload_in_test = True
        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {UploadedTrackPostFields.TRACK_FILE_PUBLIC: sample_file}
            if kwargs:
                kwargs = data_transformer.merge_two_dicts(file_field_dict, kwargs)
            else:
                kwargs = file_field_dict
            return self.api_client.post(
                path=reverse('me-uploaded-track-list'),
                data=kwargs, format='multipart', handle_response=self._set_results)

    # Defined here and not in UploadedTrackTestCase because other views needs sometimes to put a track for testing purposes
    # (testing Genre deletion for example)
    def _put_uploaded_track(self, uuid, **kwargs):
        if self.is_from_uploaded_track_test_case and self.model_class == UploadedTrack:
            return self.api_client.put(
                path=reverse('me-uploaded-track-detail', kwargs={'pk': uuid}),
                data=kwargs, format='multipart', handle_response=self._set_results)
        return self.api_client.put(
            path=reverse('me-uploaded-track-detail', kwargs={'pk': uuid}),
            data=kwargs, format='multipart')

    def _post_uploaded_track_being_logged_out(self):
        self._logout()
        return self.api_client.post(
            path=reverse('me-uploaded-track-list'), data={}, format='multipart', handle_response=self._set_results)

    def _domain_helper(self, helper_class: type) -> "AppTestCase":
        """Return a domain test case instance bound to this test's api_client and users for composition in E2E tests.
        Does not call setUp() on the helper to avoid duplicate DB fixtures (users).
        """
        inst = helper_class()
        inst.api_client = self.api_client
        inst.test_user1 = self.test_user1
        inst.test_user2 = self.test_user2
        inst.model_fixture_factory = self.model_fixture_factory
        inst.TEST_FILES_BASE_DIR = self.TEST_FILES_BASE_DIR
        inst._login_as_test_user1()
        return inst

    def _setup_system_user_for_reference_tests(self, system_username: str = "test_reference_system_user"):
        """Set up system user for reference endpoint tests and configure TMTA_USERNAME environment variable."""
        self._system_user, created = User.objects.get_or_create(
            username=system_username,
            defaults={
                "is_system": True,
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "email": "system@test.com",
                "is_test_user": True,
                "password": make_password(None),
            },
        )
        if created or not self._system_user.password.startswith("!"):
            self._system_user.set_unusable_password()
            self._system_user.save(update_fields=["password"])
        self._original_tmta_username = os.environ.get("TMTA_USERNAME")
        os.environ["TMTA_USERNAME"] = system_username
        return self._system_user

    def setUp(self, methods_names_to_implement: list[str] | None = None) -> None:

        self.test_admin_user = User.objects.create_superuser(
            username='test_admin', password='test_admin', email='test_admin@example.com', is_test_user=True)

        self.test_user1 = User.objects.create_instance(
            username='pytest_user1', password='pytest_user1', email='pytest@user1.com', is_test_user=True)

        self.test_user2 = User.objects.create_instance(
            username='pytest_user2', password='pytest_user2', email='pytest@user2.com', is_test_user=True)

        self.spotify_test_user_1 = User(username='spotify_test_user_1', email='spotify@test.com',
                                        spotify_id='spotify_test_user_1', is_test_user=True)
        self.spotify_test_user_1.set_password('spotify_test_user_1')
        self.spotify_test_user_1.save()

        self.spotify_test_user_2 = User(username='spotify_test_user_2', email='spotify@test.com',
                                        spotify_id='spotify_test_user_2', is_test_user=True)
        self.spotify_test_user_2.set_password('spotify_test_user_2')
        self.spotify_test_user_2.save()

        self.model_fixture_factory = ModelFixtureFactory(
            default_test_user=self.test_user1, test_uploaded_track_dir=self.TEST_FILES_BASE_DIR,)

        super().setUp()

        if methods_names_to_implement:
            for method_name in methods_names_to_implement:
                if not hasattr(self, method_name) or not callable(getattr(self, method_name)):
                    raise NotImplementedError(f"Subclasses must implement the '{method_name}' method")

        self.api_client = AppApiClient(test_case=self)
        self._used_upload_in_test = False
        self._login_as_test_user1()

    def tearDown(self):
        if getattr(settings, 'FILE_UPLOAD_TEMP_DIR', None):
            temp_dir = settings.FILE_UPLOAD_TEMP_DIR
            if os.path.isdir(temp_dir):
                if getattr(self, '_used_upload_in_test', False):
                    contents = os.listdir(temp_dir)
                    assert contents == [], (
                        "Temp dir not empty after test; endpoint likely did not close TemporaryUploadedFile. Left: %s"
                        % contents
                    )
                for name in os.listdir(temp_dir):
                    path = os.path.join(temp_dir, name)
                    try:
                        if os.path.isfile(path):
                            os.unlink(path)
                    except OSError:
                        pass
        if getattr(settings, "METADATA_SESSION_DIR", None):
            session_dir = settings.METADATA_SESSION_DIR
            if session_dir and os.path.isdir(session_dir):
                for name in os.listdir(session_dir):
                    path = os.path.join(session_dir, name)
                    try:
                        if os.path.isfile(path):
                            os.unlink(path)
                    except OSError:
                        pass
        if hasattr(self, '_original_tmta_username'):
            if self._original_tmta_username is not None:
                os.environ["TMTA_USERNAME"] = self._original_tmta_username
            elif "TMTA_USERNAME" in os.environ:
                del os.environ["TMTA_USERNAME"]
        super().tearDown()
