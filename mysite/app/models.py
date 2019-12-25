from django.db import models
from django.utils import timezone
import random

# Models here

class Organisation(models.Model):
	name = models.CharField(max_length=512)
	email = models.CharField(max_length=256)
	registered_on = models.DateTimeField(default=timezone.now)
	id_hash = models.CharField(max_length=64)

	def __str__(self):
		return self.name

class Params(models.Model):
	name = models.CharField(max_length=10)
	registered_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

class Certificate(models.Model):
	value = models.CharField(max_length=128)
	awarded_to = models.CharField(max_length=128)
	awarded_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.awarded_to

class User(models.Model):
	email = models.CharField(max_length=512)
	name = models.CharField(max_length=256)
	user_id = models.CharField(max_length=512)

	def __str__(self):
		return self.user_id