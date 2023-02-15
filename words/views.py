from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from LEnglish_mobile.utils import AuthenticatedMixin, NotAuthenticatedMixin, get_new_word_from_request, get_page_from_request
from users.models import UsersUsersWords
from json.decoder import JSONDecodeError
from .serializers import WordsSerializer, WordsCreateSerializer, WordsUpdateSerializer, WordsDeleteSerializer
from .models import UsersWords
from .exceptions import WordNotFound

# Create your views here.
class WordsListAPIView(AuthenticatedMixin, APIView):

	def get_queryset(self, user, page):
		start = (page - 1) * 10
		words_id = UsersUsersWords.objects.filter(users_id=user.pk)
		words = [elem["userswords_id"] for elem in words_id.values()]
		words = UsersWords.objects.filter(pk__in=words)[start:start + 10]
		return words

	def get(self, request):
		page = get_page_from_request(request)
		queryset = self.get_queryset(request.user, page)
		return Response(WordsSerializer(queryset, many=True).data)

class WordsRetrieveAPIView(AuthenticatedMixin, APIView):

	def get_queryset(self, user, id):
		try:
			users_words_obj = UsersUsersWords.objects.get(userswords_id=id)
			if users_words_obj.users_id == user.pk:
				return UsersWords.objects.get(id=id)
			else:
				raise WordNotFound()
		except UsersUsersWords.DoesNotExist:
			raise WordNotFound()

	def get(self, request, id):
		try:
			word = self.get_queryset(request.user, id)

			return Response(WordsSerializer(word).data)
		except WordNotFound:
			return Response(status=404)

class WordsCreateAPIView(AuthenticatedMixin, APIView):

	def post(self, request):
		word, translate, level = get_new_word_from_request(request)
		serializer_obj = WordsCreateSerializer(data={"word":word, "translate":translate,"user_level":level})
		if serializer_obj.is_valid():
			serialized_word = serializer_obj.create(serializer_obj.data, request)
			return Response(WordsCreateSerializer(serialized_word).data)
		else:
			return Response({"status":"Not valid data"}, status=400)

class WordsUpdateAPIView(AuthenticatedMixin, APIView):
	
	def patch(self, request, id):
		try:
			word, translate, level = get_new_word_from_request(request)
		except JSONDecodeError:
			return Response(status=400)

		serializer_obj = WordsUpdateSerializer(data={"word":word, "translate":translate, "user_level":level})
		if serializer_obj.is_valid():
			try:
				serialized_word = serializer_obj.update(serializer_obj.data, request, id)
				return Response(WordsUpdateSerializer(serialized_word).data)
			except WordNotFound:
				return Response(status=404)

		return Response(status=404)

class WordsDeleteAPIView(AuthenticatedMixin, APIView):
	
	def get(self, request, id):
		serializer_obj = WordsDeleteSerializer()
		try:
			serializer_obj.delete(request, id)
			return Response(status=200)
		except WordNotFound:
			return Response(status=404)
