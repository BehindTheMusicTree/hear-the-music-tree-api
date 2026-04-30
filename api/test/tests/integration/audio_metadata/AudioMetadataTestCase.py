from django.urls import reverse

from api.serializer.audio_metadata.Fields import Fields
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.utils import data_transformer


class AudioMetadataTestCase(AppTestCase):
    def _post_get_full_metadata(
        self,
        test_uploaded_track_filename: UploadedTrackTestFilename = UploadedTrackTestFilename.RECORDING_QUEEN_25_MATCHES_BUT_ONE_WITH_BEST_DURATION_AND_MOST_FIELDS_AND_MOST_RELEASE_GROUPS_MP3,
        **kwargs,
    ):
        self._used_upload_in_test = True
        file_abs_path = self.TEST_FILES_BASE_DIR / test_uploaded_track_filename.value

        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {Fields.FILE: sample_file}
            if kwargs:
                kwargs = data_transformer.merge_two_dicts(file_field_dict, kwargs)
            else:
                kwargs = file_field_dict

            return self.api_client.post(path=reverse("audio-metadata-full"), data=kwargs, format="multipart")
