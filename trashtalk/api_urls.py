from django.conf.urls import url

from accounts.views import UserCreateAPIView, UserListAPIView, UserDetailAPIView
from cleanups.views.api_views import (CleanupListCreateAPIView, CleanupDetailAPIView,
                                      LocationListCreateView)

urlpatterns = [
    url(r'^cleanups/$', CleanupListCreateAPIView.as_view(), name='cleanups'),
    url(r'^cleanups/(?P<pk>[0-9]+)/$', CleanupDetailAPIView.as_view(), name='cleanup-detail'),
    url(r'^locations/$', LocationListCreateView.as_view(), name='locations'),
    url(r'^users/$', UserCreateAPIView.as_view(), name='users-create'),
    url(r'^users/list/$', UserListAPIView.as_view(), name='users-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetailAPIView.as_view(), name='users-detail'),
]
