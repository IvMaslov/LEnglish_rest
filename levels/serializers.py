from rest_framework import serializers
from words.models import UsersWords, MainWords

class QuizSerializer(serializers.ModelSerializer):

	class Meta:
		model = UsersWords
		fields = [
			"id",
			"word",
			"translate",
			"user_level"
		]

class DefaultWordsSerializer(serializers.ModelSerializer):

	class Meta:
		model = MainWords
		fields = [
			"id",
			"word",
			"translate",
			"word_category"
		]

