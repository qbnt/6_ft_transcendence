from django.shortcuts	import render
from live_chat.models	import OnlineUsers

def index(request):
	online = OnlineUsers.objects.first()
	context = {
		"message": "[Ceci est le pong]",
		"online": online,
	}
	return render(request, "home/index.html", context)
