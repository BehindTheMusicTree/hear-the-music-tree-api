from dataclasses import dataclass

from hear.model.musicbrainz_resource.children.recording.MbRecording import MbRecording
from hear.model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import (
    MbRecordingMissingCause,
)


@dataclass
class MusicbrainzRecordingLookupResult:
    _recording: MbRecording | None = None
    _missing_cause: MbRecordingMissingCause | None = None

    class Meta:
        verbose_name = "MusicBrainz Recording Lookup Result"
        verbose_name_plural = "MusicBrainz Recording Lookup Results"

    def __init__(self, recording: MbRecording | None, missing_cause: MbRecordingMissingCause | None):
        self._recording = recording
        self._missing_cause = missing_cause

    @property
    def is_success(self) -> bool:
        return self._recording is not None

    @property
    def recording(self) -> MbRecording:
        if self._recording is None:
            raise ValueError(f"{self.__class__} is not successful")
        return self._recording

    @property
    def missing_cause(self) -> MbRecordingMissingCause:
        if self._missing_cause is None:
            raise ValueError(f"{self.__class__} is successful, no missing cause available")
        return self._missing_cause
