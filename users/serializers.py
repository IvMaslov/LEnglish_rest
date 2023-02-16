from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import datetime
from .models import Users
from .exceptions import UserAlreadyExist

UserModel = Users

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	def create(self, validated_data):
		user = UserModel.objects.create(username=validated_data["username"],
										email=validated_data["email"],
										is_superuser=False,
										first_name="",
										last_name="",
										is_staff=False,
										is_active=True,
										date_joined=datetime.now())
		user.set_password(validated_data["password"])
		user.save()
		return user

	class Meta:
		model = UserModel
		fields = [
			"username", 
			"email", 
			"password"
		]

class UserUpdateSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=150)

	def update(self, validated_data, request):
		excluded_data = UserModel.objects.values_list("username", "email").exclude(pk=request.user.pk)
		excluded_usernames = [elem[0] for elem in excluded_data]
		excluded_email = [elem[1] for elem in excluded_data]

		if validated_data.get("email") in excluded_email or validated_data.get("username") in excluded_usernames:
			raise UserAlreadyExist()

		user = UserModel.objects.get(pk=request.user.pk)
		user.email = validated_data.get("email")
		user.username = validated_data.get("username")
		user.first_name = validated_data.get("first_name", None)
		user.last_name = validated_data.get("last_name", None)
		user.save()
		return user

	class Meta:
		model = UserModel
		fields = [
			"username", 
			"email", 
			"first_name", 
			"last_name"
		]


class UserGetInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = [
			"username", 
			"email",
			"first_name",
			"last_name",
			"date_joined", 
			"last_login"
		]
