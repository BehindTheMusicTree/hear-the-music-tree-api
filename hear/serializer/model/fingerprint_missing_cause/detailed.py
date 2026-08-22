from rest_framework import serializers

from hear.model.uploaded_track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from hear.serializer.model.fingerprint_missing_cause.code.detailed import FingerprintMissingCauseCodeDetailedSerializer

from .Fields import Fields


class FingerprintMissingCauseDetailedSerializer(serializers.ModelSerializer):
    code = FingerprintMissingCauseCodeDetailedSerializer()

    class Meta:
        model = FingerprintMissingCause
        fields = [Fields.CODE, Fields.MESSAGE]
