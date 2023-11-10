from django.urls import path

from feeds.views import (AddFeedView, BookmarkFeedView, GetFeedView)

urlpatterns = [
    path('add/', AddFeedView.as_view(), name='add-feed'),
    path('bookmark/', BookmarkFeedView.as_view(), name='bookmark-feed'),
    path('', GetFeedView.as_view(), name='list-feeds'),
]
