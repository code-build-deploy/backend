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
	display = models.CharField(max_length=5) # this is to determine whether to display certificate or not (until it's issued it should be false. when the user wishes to keep it private it should be false (not sure about the user wanting to keep a certificate private part tho))
	people_associated = models.TextField()
	certificate_hash = models.TextField()
	certificate_hash_indexes = models.TextField()
	awarded_to = models.CharField(max_length=128)
	remarks = models.TextField()
	awarded_on = models.DateTimeField(default=timezone.now)

	def ret_certificate(self):
		if self.display == 'false':
			return False
		else:
			return True

	def check_employee(self, signedInUserName):
		if signedInUserName in self.people_associated:
			return True

	def employee_approves(self, signedInUserName):
		usernameToRemove = signedInUserName + ", "
		tempdata = self.people_associated
		if ', ' in tempdata:
			tempStr = signedInUserName + ', '
		else:
			tempStr = signedInUserName
		tempdata = tempdata.replace(tempStr, '')
		self.people_associated = tempdata
		self.save()

	def approved(self):
		if len(self.people_associated) == 0:
			return True
		else:
			return False

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


# class Employee(models.Model):
# 	name = models.CharField(max_length=128)
# 	username = models.CharField(max_length=128)
# 	email = models.CharField(max_length=256)
# 	chain = models.CharField(max_length=256)
# 	user_id = models.CharField(max_length=512)
# 	organisation_associated = models.TextField()

# 	def validate_chain(self, recieved_chain):
# 		if recieved_chain == self.chain:
# 			return True
# 		else:
# 			return False

# 	def check_organisation(self, tempOrganisationName):
# 		if tempOrganisationName in self.organisation_associated:
# 			return True
# 		else:
# 			return False

# 	def __str__(self):
# 		return self.name



# End here