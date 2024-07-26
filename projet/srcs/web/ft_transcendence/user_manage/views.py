from django.shortcuts	import render
from django.http		import HttpResponse
from .models			import User


def usr_list(request):
	return render(request, 'user_manage/usr_view.html')

def usr_view(request):
	pass

def usr_create(request):
	pass

def usr_edit(request):
	pass

def usr_suppr(request):
	pass

def usr_connect(request):
	pass