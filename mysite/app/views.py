from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Param, User, Certificate, Organisation
import random
import json
from datetime import datetime
# Create your views here.


# Autosave function (Used this to create worded parameters I guess)
def autosave(request):
	source_file = open("words_dictionary.json")
	data = json.load(source_file)
	for i in data.keys():
		if len(i) >= 5 and len(i) <= 8:
			Param.objects.create(name=i)
	return HttpResponse("<h1>Successful</h1>")


def home(request):
	return HttpResponse("Hello World")

def display(request):
	if request.method == 'POST':
		resp = json.loads(request.body)
		tempEmail = resp['email']
		tempUser = User.objects.get(email=tempEmail)
		merits = Certificate.objects.filter(awarded_to=tempUser.username)
		awarded = []
		count = 0
		for i in merits:
			if i.ret_certificate():
				data = {
					"title": i.title,
					"reciever": i.awarded_to,
					"time": i.awarded_on
				}
				count = count + 1
				awarded.append(data)
			titles = {
				"certificates": awarded
			}
		return JsonResponse(titles, safe=False)
	else:
		return HttpResponse("Nopes bud, not working")

def generate_words(words):
	x = list(Param.objects.values('name'))
	for i in range(len(x)):
		word = x[i]['name']
		words.append(word)

def randomise_hash(words):
	indexes = []
	random_chain = []
	while True:
		if len(random_chain) == 10:
			break
		x = random.random() * 9
		x = round(x)
		if x not in indexes:
			indexes.append(x)
			random_chain.append(words[x])
	return random_chain, indexes

def create_hash(username, email, reqtype):
	words = []
	generate_words(words)
	hash_selected_index = []
	sel_words = []
	li = ""
	while len(hash_selected_index) != 10:
		x = random.random() * (len(words) - 1)
		x = round(x)
		if x not in hash_selected_index:
			hash_selected_index.append(x)
			sel_words.append(words[x])

	final_generated_chain, final_hash_index = randomise_hash(sel_words)

	string = ""
	random_string = ""
	
	count = 0
	
	for i in sel_words:
		string = string + i
		if count < 9:
			string = string + " "
		count = count + 1

	count = 0

	for i in final_generated_chain:
		random_string = random_string + i
		if count < 9:
			random_string = random_string + " "
		count = count + 1

	id_list = ""
	count = 0

	for i in final_hash_index:
		id_list = id_list + str(i)
		if count < 9:
			id_list = id_list + " "
		count = count + 1

	if reqtype == 'user':
		User.objects.create(email=email, username=username, user_id=id_list, chain=string)
	elif reqtype == 'org':
		Organisation.objects.create(name=username, email=email, user_id=id_list, id_hash=string)
	else:
		Certificate.objects.create(title=username, display='false', people_associated=email, awarded_to=reqtype, certificate_hash=string, certificate_hash_indexes=id_list)

	return random_string

def register_user(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		email = y["email"]
		username = y["username"]
		id_hash = create_hash(username, email, 'user')
		data = {
			"username": username,
			"email": email,
			"hash": id_hash
		}
		return JsonResponse(data, safe=False)
	else:
		return HttpResponse("Incorrect validation schema")

def login(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		requested_email = y["email"]
		requested_username = y["username"]
		recieved_chain = y["chain"]
		recieved_chain = recieved_chain.split()
		
		user = User.objects.get(username=requested_username, email=requested_email)
		indexes = user.user_id
		indexes = indexes.split()

		for i in range(len(indexes)):
			indexes[i] = int(indexes[i])
		
		data =[]
		for i in range(10):
			data.append(" ")

		for i in range(10):
			data[indexes[i]] = recieved_chain[i]

		new_chain = ""

		for i in range(10):
			new_chain = new_chain + data[i]
			if i < 9:
				new_chain = new_chain + " "
		
		if user.validate_chain(new_chain):
			data = {
				"val": "True"
			}
			return JsonResponse(data, safe=True)
		else:
			data = {
				"val": "False"
			}
			return JsonResponse(data, safe=False)
	else:
		return HttpResponse("Incorrect Attempt")

def register_organisation(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		name = y["name"]
		email = y["email"]
		id_hash = create_hash(name, email, 'org')
		data = {
			"name": name,
			"email": email,
			"hash": id_hash
		}
		return JsonResponse(data, safe=False)
	else:
		return HttpResponse("Incorrect validation schema")

def organisation_login(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		organisation_username = y["name"]
		organisation_email = y["email"]
		organisation_hash = y["chain"]
		recieved_chain = organisation_hash.split()
		
		organisation = Organisation.objects.get(name=organisation_username, email=organisation_email)
		indexes = organisation.user_id
		indexes = indexes.split()

		for i in range(len(indexes)):
			indexes[i] = int(indexes[i])
		
		data =[]
		for i in range(10):
			data.append(" ")

		for i in range(10):
			data[indexes[i]] = recieved_chain[i]

		count = 0
		new_chain = ""

		for i in range(10):
			new_chain = new_chain + data[i]
			if count < 9:
				new_chain = new_chain + " "
			count = count + 1
		
		if organisation.validate_chain(new_chain):
			data = {
				"login": "true"
			}
			return JsonResponse(data, safe=True)
		else:
			data = {
				"login": "false"
			}
			return JsonResponse(data, safe=True)
	else:
		return HttpResponse("Attempt")


def create_cert(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		organisation_username = y["name"]
		organisation_email = y["email"]
		organisation_hash = y["chain"]
		temp_cert_title = y["title"]
		temp_cert_people = y["people"]
		temp_cert_awarded_to = y["assigned"]
		recieved_chain = organisation_hash.split()
		
		organisation = Organisation.objects.get(name=organisation_username, email=organisation_email)
		indexes = organisation.user_id
		indexes = indexes.split()
		new_indexes = [int(i) for i in indexes]

		for i in range(len(indexes)):
			indexes[i] = int(indexes[i])
		print(indexes, new_indexes)
		data =[]
		for i in range(10):
			data.append(" ")

		for i in range(10):
			data[indexes[i]] = recieved_chain[i]

		count = 0
		new_chain = ""

		for i in range(10):
			new_chain = new_chain + data[i]
			if count < 9:
				new_chain = new_chain + " "
			count = count + 1
		
		if organisation.validate_chain(new_chain):
			id_hash = create_hash(temp_cert_title, temp_cert_people, temp_cert_awarded_to)
			data = {
				"result": "okay"
			}
			return JsonResponse(data, safe=True)
		else:
			data = {
				"result": "unsuccessful"
			}
			return JsonResponse(data, safe=True)
	else:
		return HttpResponse("Attempt")

def dashboard(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		tempusername = y["username"]
		records = Certificate.objects.all()
		certificates_to_be_signed = []
		for i in records:
			if i.check_employee(tempusername):
				data = {
					"title": i.title,
					"reciever": i.awarded_to,
					"time": i.awarded_on,
					"hash": i.certificate_hash
				}
				certificates_to_be_signed.append(data)
		return JsonResponse(certificates_to_be_signed, safe=False)
	else:
		return HttpResponse("Invalid")


def sign_certificate(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		tempCertificateHash = y["hash"]
		tempUsername = y["username"]
		tempRemarks = y["remarks"]
		tempStatus = y["status"]
		approvedCertificate = Certificate.objects.get(certificate_hash=tempCertificateHash)
		if tempStatus == 'Approved':
			remarks = "\n" + tempUsername + " approves this."
			approvedCertificate.employee_approves(tempUsername)
		else:
			currDateTime = datetime.now()
			timestamp = currDateTime.strftime("%d-%b-%Y, %H:%M")
			remarks = "\n" + tempUsername + " says '" + tempRemarks + "' at " + timestamp
		approvedCertificate.remarks = approvedCertificate.remarks + remarks
		if approvedCertificate.approved():
			approvedCertificate.display = 'true'
		approvedCertificate.save()
		data = {
			"message": "success"
		}
		return JsonResponse(data, safe=False)
	else:
		data = {
			"message": "Try again bud"
		}
		return JsonResponse(data, safe=False)

