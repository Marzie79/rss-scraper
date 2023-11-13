from django.urls import path

from feeds.views import (AddFeedView, BookmarkFeedView, GetFeedView,
                         CommentFeedView)

urlpatterns = [
    path('add/', AddFeedView.as_view(), name='add-feed'),
    path('comment/', CommentFeedView.as_view(), name='comment-feed'),
    path('bookmark/', BookmarkFeedView.as_view(), name='bookmark-feed'),
    path('', GetFeedView.as_view(), name='list-feeds'),
]
