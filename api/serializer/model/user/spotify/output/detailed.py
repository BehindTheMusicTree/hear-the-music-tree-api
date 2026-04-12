from rest_framework import serializers

from api.model.user.User import User

from .Fields import Fields


class SpotifyUserDetailedSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    uri = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            Fields.SPOTIFY_ID,
            Fields.EMAIL,
            Fields.SPOTIFY_PROFILE,
            Fields.DISPLAY_NAME,
            Fields.FOLLOWERS,
            Fields.HREF,
            Fields.IMAGES,
            Fields.TYPE,
            Fields.URI,
            Fields.SPOTIFY_LIBRARY_LAST_SYNCED_AT,
        ]

    def get_display_name(self, obj: User):
        return obj.spotify_profile.get("display_name") if obj.spotify_profile else None

    def get_followers(self, obj: User):
        return obj.spotify_profile.get("followers") if obj.spotify_profile else None

    def get_href(self, obj: User):
        return obj.spotify_profile.get("href") if obj.spotify_profile else None

    def get_images(self, obj: User):
        return obj.spotify_profile.get("images") if obj.spotify_profile else None

    def get_type(self, obj: User):
        return obj.spotify_profile.get("type") if obj.spotify_profile else None

    def get_uri(self, obj: User):
        return obj.spotify_profile.get("uri") if obj.spotify_profile else None
