from django.urls import path
from .views import *

urlpatterns = [
	path("quiz", QuizListAPIView.as_view(), name='quiz'),
	path("levels/<slug:slug_id>", LevelsListAPIView.as_view(), name='levels'),
	path("words/<slug:slug_id>", DeafultWordsAPIView.as_view(), name='default_words')
]