from rest_framework.response import Response
from rest_framework import (status, generics)

from feeds.modules.logics.mongo_interface import (add_bookmark, add_comment,
                                                  get_account_feeds,
                                                  save_feeds)
from feeds.serializers import (AddFeedSerializer, BookmarkFeedSerializer,
                               CommentFeedSerializer)
from utilities.exceptions import MultiLanguageException
from utilities.messages.error import INVALID_INPUT


class AddFeedView(generics.GenericAPIView):
    """API view for adding a new feed."""
    serializer_class = AddFeedSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        save_feeds(account_id=request.user.id, **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class BookmarkFeedView(generics.GenericAPIView):
    """API view for bookmarking a feed."""
    serializer_class = BookmarkFeedSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['account_id'] = request.user.id

        add_bookmark(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class CommentFeedView(generics.GenericAPIView):
    """API view for commenting on a feed."""
    serializer_class = CommentFeedSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['account_id'] = request.user.id

        add_comment(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class GetFeedView(generics.GenericAPIView):
    """API view for retrieving paginated feed data for the user."""

    def get(self, request):
        try:
            offset = int(request.GET.get('offset', 1))
            limit = int(request.GET.get('limit', 4))
        except (ValueError, TypeError):
            raise MultiLanguageException(INVALID_INPUT)

        return Response(data=get_account_feeds(limit=limit,
                                               offset=offset,
                                               account_id=request.user.id),
                        status=status.HTTP_200_OK)
