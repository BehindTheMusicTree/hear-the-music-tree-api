from the_music_tree_api_kit.public_standard_resource.PublicStandardResource import PublicStandardResource

from api.model.field.AppCharField import AppCharField


class SpotifyResource(PublicStandardResource):
    spotify_id = AppCharField(max_length=50, unique=True, null=False, blank=False, primary_key=True)

    class Meta:
        abstract = True
