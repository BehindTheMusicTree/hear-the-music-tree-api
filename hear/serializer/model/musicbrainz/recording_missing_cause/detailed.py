from rest_framework import serializers

from hear.model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import (
    Fields as ModelFields,
)
from hear.model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import (
    MbRecordingMissingCause,
)


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    CODE = ModelFields.CODE
    LABEL = ModelFields.MESSAGE


class MusicbrainzRecordingMissingCauseDetailedSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(source=Fields.CODE)

    class Meta:
        model = MbRecordingMissingCause
        fields = [Fields.CODE, Fields.LABEL]
