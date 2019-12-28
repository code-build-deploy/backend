from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Params, User, Certificate, Organisation
import random
import json
# Create your views here.

# selected_words = ['bedposts', 'nonactor', 'clothing', 'gridlock', 'cochlear', 'challies', 'expiatory', 'symbions', 'lucernes', 'formants', 'unguents', 'amassers', 'deponing', 'chimaera', 'scattier', 'diastral', 'foveolar', 'swannery', 'pumicing', 'mystagogy']

# Autosave function (Used this to create worded parameters I guess)
# def autosave(request):
# 	i = 0
# 	while i < 20:
# 		x = selected_words[i]
# 		Params.objects.create(name=x)
# 		i = i + 1
# 	return HttpResponse("<h1>Successful</h1>")

# Work on the register_user_request later, we'll use this for three way handshake

# def register_user_request(request):
# 	if request.method == 'POST':
# 		y = json.loads(request.body)
# 	else:
# 		return HttpResponse("Incorrect validation schema")

selected_words = []

def home(request):
	return HttpResponse("Hello World")

def display(request):
	if request.method == 'POST':
		resp = json.loads(request.body)
		user_hash_associated = resp['hash']
		merits = Certificate.objects.filter(awarded_to=user_hash_associated)
		for i in merits:
			print(i.ret_certificate())
		data = {
			"number": int(len(merits))
		}
		return JsonResponse(data, safe=False)
	else:
		return HttpResponse("Nopes bud, not working")

def generate_words():
	x = list(Params.objects.values('name'))
	for i in range(len(x)):
		word = x[i]['name']
		selected_words.append(word)

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
	generate_words()
	hash_selected_index = []
	words = []
	li = ""
	while len(hash_selected_index) != 10:
		x = random.random() * (len(selected_words) - 1)
		x = round(x)
		if x not in hash_selected_index:
			hash_selected_index.append(x)
			words.append(selected_words[x])

	final_generated_chain, final_hash_index = randomise_hash(words)

	string = ""
	random_string = ""
	
	count = 0
	
	for i in words:
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

		count = 0
		new_chain = ""

		for i in range(10):
			new_chain = new_chain + data[i]
			if count < 9:
				new_chain = new_chain + " "
			count = count + 1
		
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
		organisation_username = y["username"]
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

