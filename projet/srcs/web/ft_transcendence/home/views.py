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
	return render(request, "home/index.html", context)