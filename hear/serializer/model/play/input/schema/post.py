from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from hear.model.play.Play import Play
from hear.serializer.field.foreign_key.UserContentObjectUuidField import PrivateContentUuidField

from .PostFields import Fields as PostFields
from .SchemaFields import Fields as SchemaFields


class PlayPostSerializer(AppInputSerializer, serializers.ModelSerializer):
    content = PrivateContentUuidField(write_only=True)

    class Meta:
        model = Play
        fields = [PostFields.CONTENT]

    def validate(self, attrs: dict) -> dict:
        content_data = attrs.pop(PostFields.CONTENT)
        attrs[SchemaFields.CONTENT_TYPE] = content_data[SchemaFields.CONTENT_TYPE]
        attrs[SchemaFields.CONTENT] = content_data[SchemaFields.CONTENT]
        return attrs
