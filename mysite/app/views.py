from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Params
import random
import json
# Create your views here.

# selected_words = ['bedposts', 'nonactor', 'clothing', 'gridlock', 'cochlear', 'challies', 'expiatory', 'symbions', 'lucernes', 'formants', 'unguents', 'amassers', 'deponing', 'chimaera', 'scattier', 'diastral', 'foveolar', 'swannery', 'pumicing', 'mystagogy']
selected_words = []

def home(request):
	return HttpResponse("Hello World")

# def autosave(request):
# 	i = 0
# 	while i < 20:
# 		x = selected_words[i]
# 		Params.objects.create(name=x)
# 		i = i + 1
# 	return HttpResponse("<h1>Successful</h1>")

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

def create_hash(request):
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

	# temp = []
	
	# for i in range(10):
	# 	for j in range(10):
	# 		if final_hash_index[j] == i:
	# 			break
	# 	temp.append(final_generated_chain[j])

	# print(temp, words)

	return JsonResponse(final_generated_chain, safe=False)

def login(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		temp = y["chain"]
		requested_email = y["email"]

		# figure out how to use emails and chain, for the certificate identification

		chain = temp.split()
		print(chain)
		return HttpResponse("Successful")
	else:
		return HttpResponse("Try again")

def generate_certificate(request):
	if request.method == 'POST':
		y = json.loads(request.body)
		data = ""
		data = data + y["name"]
		return HttpResponse(data)
	else:
		return HttpResponse("Attempt")


# def clash(request):
# 	flag = 0
# 	i = 0
# 	for i in range(20):
# 		x = selected_words[i]
# 		count = 0
# 		j = 0
# 		for j in range(20):
# 			if x == selected_words[j]:
# 				count = count + 1
# 		if count >= 2:
# 			flag = 1
# 			break

# 	if flag == 1:
# 		resp = "Found clashing words at " + selected_words[i]
# 		return HttpResponse(resp)

# 	else:
# 		return HttpResponse("All clear ?")