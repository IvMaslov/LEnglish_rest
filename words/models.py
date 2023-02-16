from django.db import models
from django.urls import reverse

class MainLevels(models.Model):
	level = models.CharField(max_length=100)
	slug = models.CharField(unique=True, max_length=100)

	def __repr__(self):
		return "Level with name: <{word}>".format(word=self.level)

	def get_absolute_url(self):
		return reverse("level", kwargs={"slug_id": self.slug})


class MainWords(models.Model):
	word = models.CharField(max_length=70)
	translate = models.CharField(max_length=70)
	word_category = models.ForeignKey(MainLevels, models.DO_NOTHING, blank=True, null=True)

	def __repr__(self):
		return "Word with name: <{word}>".format(word=self.word)

class UsersWords(models.Model):
	word = models.CharField(max_length=100)
	translate = models.CharField(max_length=100)
	user_level = models.ForeignKey(MainLevels, models.CASCADE,blank=True, null=True)

	def __repr__(self):
		return "Word with name: <{word}>".format(word=self.word)