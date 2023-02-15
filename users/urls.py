from django.urls import path
from .views import *

urlpatterns = [
	path("profile", UserRetrieveAPIView.as_view(), name="profile"),
	path("profile/update", UserUpdateAPIView.as_view(), name="profile_update"),
]