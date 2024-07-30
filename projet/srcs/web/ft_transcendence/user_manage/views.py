from django.contrib.auth			import authenticate, login, logout
from django.contrib.auth.forms		import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators	import login_required
from django.contrib					import messages
from django.shortcuts				import render, redirect
from .forms							import CustomUserUpdateForm, CustomUserCreationForm, ProfileForm
from .models						import Profile

# -------------------------Creation et connections---------------------------- #

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

def register_user(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)  # Connexion de l'utilisateur après l'enregistrement
            return redirect("home:index")
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, "user_manage/register.html", {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# ------------------------------Edition--------------------------------------- #

@login_required
def edit_user(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect("home:index")
    else:
        user_form = CustomUserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'user_manage/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def pw_update(request):
	user = request.user
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			login(request, user)
			messages.success(request, 'Votre mot de passe a bien été mis à jour.')
			return redirect('home:index')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'user_manage/pw_update.html', {'form': form})