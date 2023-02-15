from django.urls import path
from .views import *

urlpatterns = [
	path("words", WordsListAPIView.as_view(), name="words"),
	path("words/<int:id>", WordsRetrieveAPIView.as_view(), name="words_id"),
	path("words/create", WordsCreateAPIView.as_view(), name="create_word"),
	path("words/update/<int:id>", WordsUpdateAPIView.as_view(), name="update_word"),
	path("words/delete/<int:id>", WordsDeleteAPIView.as_view(), name="delete_word")
]