from api.model.musicbrainz_resource.children.recording.MbRecording import Fields as ModelFields
from api.model.musicbrainz_resource.children.recording.MbRecording import MbRecording
from api.serializer.AppModelSerializer import AppModelSerializer
from api.serializer.model.musicbrainz.artist.detailed import MusicbrainzArtistDetailedSerializer


class Fields:
    MUSICBRAINZ_ID = ModelFields.MUSICBRAINZ_ID
    TITLE = ModelFields.TITLE
    SCORE = ModelFields.SCORE
    MUSICBRAINZ_ARTISTS = ModelFields.MUSICBRAINZ_ARTISTS
    MUSICBRAINZ_LINK = ModelFields.MUSICBRAINZ_LINK
    DURATION_IN_SEC = ModelFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ModelFields.DURATION_STR_IN_HOUR_MIN_SEC
    RELEASE_DATE = ModelFields.RELEASE_DATE


class MusicbrainzRecordingDetailedSerializer(AppModelSerializer):
    musicbrainz_artists = MusicbrainzArtistDetailedSerializer(many=True)

    class Meta:
        model = MbRecording
        fields = [
            Fields.MUSICBRAINZ_ID,
            Fields.TITLE,
            Fields.SCORE,
            Fields.MUSICBRAINZ_ARTISTS,
            Fields.MUSICBRAINZ_LINK,
            Fields.DURATION_IN_SEC,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.RELEASE_DATE,
        ]
