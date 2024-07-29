from django.contrib.auth			import authenticate, login, logout
from django.contrib.auth.forms		import AuthenticationForm
from django.contrib.auth.models		import User
from django.contrib.auth.decorators	import login_required
from django.contrib					import messages
from django.shortcuts				import render, redirect
from .forms							import CustomUserUpdateForm, CustomUserCreationForm


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
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("home:index")
	else:
		form = CustomUserCreationForm()

	return render(request, "user_manage/register.html", {'form': form})

@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Vos informations ont été mises à jour avec succès.')
            return redirect('home:index')
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'user_manage/edit.html', {'form': form})