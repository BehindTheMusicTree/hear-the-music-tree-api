from the_music_tree_api_kit.public_standard_resource.PublicStandardResource import PublicStandardResource

from api import settings
from api.model.field.AppCharField import AppCharField


class MusicbrainzResource(PublicStandardResource):
    musicbrainz_id = AppCharField(max_length=settings.MB_ID_LEN_MAX, unique=True)

    class Meta:
        abstract = True
