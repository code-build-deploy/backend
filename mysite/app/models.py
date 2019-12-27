from django.db import models
from django.utils import timezone
import random

# Models here

class Organisation(models.Model):
	name = models.CharField(max_length=512)
	email = models.CharField(max_length=256)
	registered_on = models.DateTimeField(default=timezone.now)
	id_hash = models.CharField(max_length=64)
	user_id = models.CharField(max_length=512)
	
	def validate_chain(self, recieved_chain):
		if recieved_chain == self.id_hash:
			return True
		else:
			return False
	
	def __str__(self):
		return self.name

class Params(models.Model):
	name = models.CharField(max_length=10)
	registered_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

class Certificate(models.Model):
	title = models.CharField(max_length=128)
	display = models.CharField(max_length=5)
	people_associated = models.TextField()
	certificate_hash = models.TextField()
	certificate_hash_indexes = models.TextField()
	awarded_to = models.CharField(max_length=128)
	awarded_on = models.DateTimeField(default=timezone.now)

	def ret_certificate(self):
		return bool(self.display)

	def __str__(self):
		return self.awarded_to

class User(models.Model):
	email = models.CharField(max_length=512)
	username = models.CharField(max_length=256)
	chain = models.CharField(max_length=256)
	user_id = models.CharField(max_length=512)

	def validate_chain(self, recieved_chain):
		if recieved_chain == self.chain:
			return True
		else:
			return False

	def __str__(self):
		return self.username