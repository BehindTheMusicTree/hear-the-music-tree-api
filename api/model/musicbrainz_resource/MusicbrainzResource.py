from the_music_tree_api_kit.field.AppCharField import AppCharField
from the_music_tree_api_kit.public_standard_resource.PublicStandardResource import PublicStandardResource

from api import settings


class MusicbrainzResource(PublicStandardResource):
    musicbrainz_id = AppCharField(max_length=settings.MB_ID_LEN_MAX, unique=True)

    class Meta:
        abstract = True
