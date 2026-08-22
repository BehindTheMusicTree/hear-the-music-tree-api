from the_music_tree_api_kit.public_standard_resource.PublicStandardResource import PublicStandardResource
from the_music_tree_api_kit.uuid.UuidModel import UuidModel


class PublicUniqueResource(PublicStandardResource, UuidModel):
    class Meta:
        abstract = True
