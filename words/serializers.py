from rest_framework import serializers
from rest_framework.reverse import reverse
from users.models import UsersUsersWords
from .models import UsersWords
from .exceptions import WordNotFound

class WordsSerializer(serializers.ModelSerializer):
	class Meta:
		model = UsersWords
		fields = [
			'id',
			'word',
			'translate',
			'user_level'
		]

class WordsCreateSerializer(serializers.ModelSerializer):

	def create(self, validated_data, request):
		word = UsersWords(word=validated_data.get("word").title(),
						 translate=validated_data.get("translate").title(),
						 user_level=validated_data.get("user_level"))
		word.save()
		# users_words = UsersUsersWords(users_id=request.user.pk, userswords_id=word.pk)
		# users_words.save()
		request.user.words.add(word)
		return word

	class Meta:
		model = UsersWords
		fields = [
			'id',
			'word',
			'translate',
			'user_level',
		]

class WordsUpdateSerializer(serializers.ModelSerializer):

	def update(self, validated_data, request, id):
		# words_id = UsersUsersWords.objects.filter(users_id=request.user.pk)
		# words_id = [elem.userswords_id for elem in words_id]
		# if id in words_id:
		# 	word = UsersWords.objects.get(pk=id)
		# 	word.word = validated_data.get("word")
		# 	word.translate = validated_data.get("translate")
		# 	word.user_level = validated_data.get("user_level", None)
		# 	word.save()
		# 	return word
		# raise WordNotFound()

		try:
			words_id = request.user.words.get(pk=id)
			words_id.word = validated_data.get("word")
			words_id.translate = validated_data.get("translate")
			words_id.user_level = validated_data.get("user_level", None)
			words_id.save()
			return words_id
		except Users.DoesNotExist:
			return WordNotFound()
		except UsersWords>DoesNotExist:
			return WordNotFound()


	class Meta:
		model = UsersWords
		fields = [
			'id',
			'word',
			'translate',
			'user_level',
		]

class WordsDeleteSerializer(serializers.Serializer):

	def delete(self, request, id):
		# words_id = UsersUsersWords.objects.filter(users_id=request.user.pk)
		# words_id = [elem.userswords_id for elem in words_id]
		# if id in words_id:
		# 	word = UsersWords.objects.get(pk=id)
		# 	word.delete()
		# 	return True
		# raise WordNotFound()

		try:
			words_id = request.user.words.get(pk=id)
			request.user.words.remove(words_id)
			return True
		except Users.DoesNotExist:
			return WordNotFound()
		except UsersWords.DoesNotExist:
			return WordNotFound()