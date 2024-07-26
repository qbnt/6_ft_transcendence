from django.shortcuts	import render, redirect
from django.http		import HttpResponse
from django.template	import loader

def index(request):
	context = {"message": "[Ceci est le pong]"}
	template = loader.get_template("home/index.html")
	return HttpResponse(template.render(context, request))