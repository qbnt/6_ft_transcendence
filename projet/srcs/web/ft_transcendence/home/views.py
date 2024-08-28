from django.shortcuts	import render, redirect
from django.http		import HttpResponse
from django.template	import loader
from live_chat.models	import OnlineUsers

def index(request):
	online = OnlineUsers.objects.first()
	context = {
		"message": "[Ceci est le pong]",
		"online": online,
	}
	template = loader.get_template("home/index.html")
	return HttpResponse(template.render(context, request))