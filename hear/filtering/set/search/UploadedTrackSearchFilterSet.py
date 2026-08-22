from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as UploadedTrackFields

from .SearchFilterSet import SearchFilterSet


class UploadedTrackSearchFilterSet(SearchFilterSet):
    class Meta(SearchFilterSet.Meta):
        model = UploadedTrack
        search_fields = [UploadedTrackFields.TITLE.value]
