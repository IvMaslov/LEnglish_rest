from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import json

class AuthenticatedMixin:
	permission_classes = [IsAuthenticated]
	authentication_classes = [JWTAuthentication]

	def check_user(self, request, user):
		if request.user.email == user.email:
			return True 
		return False

class NotAuthenticatedMixin:
	permission_classes = [AllowAny]



def get_user_info_from_request(request):
	json_data = json.loads(request.body.decode("utf-8"))
	email = json_data.get("email")
	username = json_data.get("username")
	password = json_data.get("password")

	return email, username, password

def get_update_user_info(request):
	json_data = json.loads(request.body.decode("utf-8"))
	email = json_data.get("email")
	username = json_data.get("username")
	first_name = json_data.get("first_name")
	last_name = json_data.get("last_name")

	return email, username, first_name, last_name

def get_new_word_from_request(request):
	json_data = json.loads(request.body.decode("utf-8"))
	word = json_data.get("word")
	translate = json_data.get("translate")
	level = json_data.get("user_level")

	return word, translate, level

def get_reverse_from_request(request):
	reverse = request.GET.get("reverse")
	if reverse == "True":
		reverse = True
	else:
		reverse = False
	return reverse

def get_page_from_request(request):
	page = request.GET.get("page")
	try:
		page = int(page)
		if page < 1:
			page = 1
	except ValueError:
		return 1
	except TypeError:
		return 1
	else:
		return page

def get_current_user(username=None, email=None):
	if username:
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = None
		return user
	elif email:
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			user = None
		return user
	else:
		return None

class DataMixin:

	def get_context_data(self, **kwargs):
		return kwargs