from rest_framework import serializers


class VideoLinkSerializer(serializers.Serializer):
    link = serializers.URLField(required=False)
    links = serializers.ListField(
        child=serializers.URLField(),
        required=False
    )

    def validate(self, data):
        if not data.get('link') and not data.get('links'):
            raise serializers.ValidationError("You must provide either a link or a list of links.")
        return data
