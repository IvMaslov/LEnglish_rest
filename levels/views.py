from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from LEnglish_mobile.utils import AuthenticatedMixin, NotAuthenticatedMixin, get_reverse_from_request, get_page_from_request
from users.models import UsersUsersWords
from words.models import UsersWords, MainWords, MainLevels
from random import sample
from .serializers import QuizSerializer, DefaultWordsSerializer

# Create your views here.


class QuizListAPIView(AuthenticatedMixin, APIView):
	def get_queryset(self, request):
		words_id = UsersUsersWords.objects.filter(users_id=request.user.pk)
		words = [elem["userswords_id"] for elem in words_id.values()]
		words = UsersWords.objects.filter(pk__in=words)
		return words

	def get(self, request):
		reverse = get_reverse_from_request(request)
		words = self.get_queryset(request)
		if len(words) < 4:
			return Response({"status":"Too few words"})
		random_4_words = sample(list(words), k=4)

		if not reverse:
			return Response(QuizSerializer(random_4_words, many=True).data)
		else:
			serializer_obj = QuizSerializer(random_4_words, many=True).data
			for elem in serializer_obj:
				elem["word"], elem["translate"] = elem["translate"], elem["word"]
			return Response(serializer_obj)

class LevelsListAPIView(NotAuthenticatedMixin, APIView):
	def get_queryset(self, slug_id):
		words = MainWords.objects.filter(word_category_id=slug_id.pk)
		return words


	def get(self, request, slug_id):
		reverse = get_reverse_from_request(request)

		slug_id = get_object_or_404(MainLevels, slug=slug_id)
		words = self.get_queryset(slug_id)

		random_4_words = sample(list(words), k=4)

		if not reverse:
			return Response(DefaultWordsSerializer(random_4_words, many=True).data)
		else:
			serializer_obj = DefaultWordsSerializer(random_4_words, many=True).data
			for elem in serializer_obj:
				elem["word"], elem["translate"] = elem["translate"], elem["word"]
			return Response(serializer_obj)

class DeafultWordsAPIView(NotAuthenticatedMixin, APIView):
	def get_queryset(self, slug_id, page):
		start = (page - 1) * 10
		words = MainWords.objects.filter(word_category_id=slug_id.pk)[start:start + 10]
		return words

	def get(self, request, slug_id):
		page = get_page_from_request(request)

		slug_id = get_object_or_404(MainLevels, slug=slug_id)
		words = self.get_queryset(slug_id, page)

		return Response(DefaultWordsSerializer(words, many=True).data)