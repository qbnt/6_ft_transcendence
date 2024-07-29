from django.contrib.auth.forms	import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth		import authenticate, login, logout
from django.contrib				import messages
from django.shortcuts			import render, redirect


def	login_user(request):
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]

		user = authenticate(request, username = username, password = password)

		if user is not None:
			login(request, user)
			return redirect("home:index")
		else:
			messages.info(request, "Identifiant ou mot de passe incorrect.")

	form = AuthenticationForm()
	return render(request, "user_manage/login.html", {'form': form})

def	logout_user(request):
	logout(request)
	return redirect("home:index")

def	register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("home:index")
	else:
		form = UserCreationForm()

	return render(request, "user_manage/register.html", {'form': form})