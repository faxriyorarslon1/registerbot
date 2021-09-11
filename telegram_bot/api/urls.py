from django.urls import path, re_path
from .views import UserList, UserDetail


urlpatterns = [
    path('list/', UserList.as_view(), name="user_list"),
    re_path(r'^(?P<pk>\d+)/detail/$', UserDetail.as_view(), name="user_detail"),
]