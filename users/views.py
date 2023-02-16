from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from json.decoder import JSONDecodeError
from LEnglish_mobile.utils import AuthenticatedMixin, NotAuthenticatedMixin, get_update_user_info
from .serializers import *
from .models import Users
from .exceptions import UserAlreadyExist


# Create your views here.
class UserCreateAPIView(NotAuthenticatedMixin, generics.CreateAPIView):
	model = Users
	serializer_class = UserSerializer

class UserRetrieveAPIView(AuthenticatedMixin, APIView):

	def initial(self, request, *args, **kwargs):
		self.model = Users
		super().initial(request, *args, **kwargs)

	def get(self, request):
		try:
			user = self.model.objects.get(username=request.user.username)
			serializer_obj = UserGetInfoSerializer(user)
			return Response(serializer_obj.data)

		except self.model.DoesNotExist:
			return Response(status=404)

class UserUpdateAPIView(AuthenticatedMixin, APIView):

	def patch(self, request):
		try:
			email, username, first_name, last_name = get_update_user_info(request)
		except JSONDecodeError:
			return Response(status=400)

		serializer_obj = UserUpdateSerializer(data={
			"email": email,
			"username": username,
			"first_name": first_name,
			"last_name": last_name
		})
		print(serializer_obj)
		if serializer_obj.is_valid():
			try:
				user = serializer_obj.update(serializer_obj.data, request)
				return Response(UserUpdateSerializer(user).data)
			except UserAlreadyExist:
				return Response({"status":"User Already Exists"}, status=409)
		return Response(status=404)

class TestAuthAPIView(AuthenticatedMixin, APIView):

	def get(self, request, *args, **kwargs):
		if (request.user.is_authenticated):
			return Response({"status": "authenticated"})

class LogoutAPIView(AuthenticatedMixin, APIView):

	def post(self, request):
		try:
			refresh_token = request.data["refresh"]
		except KeyError:
			return Response(status=400)
		try:
			token = RefreshToken(refresh_token)
			token.blacklist()
		except TokenError:
			pass
		
		return Response()