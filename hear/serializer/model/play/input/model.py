from rest_framework import serializers

from hear.model.play.Fields import Fields
from hear.model.play.Play import Play


class PlayModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_OBJECT_TYPE, Fields.CONTENT_PK]
