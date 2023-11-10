from rest_framework import serializers


class AddFeedSerializer(serializers.Serializer):
    """Validating and deserializing data related to adding a new feed."""
    rss = serializers.CharField()


class BookmarkFeedSerializer(serializers.Serializer):
    """Validating and deserializing data related to bookmarking a feed."""
    id = serializers.CharField()
    bookmark = serializers.BooleanField()
