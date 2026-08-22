from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from hear.model.playlist.Fields import Fields as PlayListFields


class ChildPlaylistModelSerializer(AppInputSerializer, serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data[PlayListFields.USER] = user
        return super().create(validated_data)
