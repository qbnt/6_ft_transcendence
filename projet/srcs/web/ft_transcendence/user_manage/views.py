from django.contrib.auth			import authenticate, login, logout
from django.contrib.auth.forms		import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators	import login_required
from django.core.files 				import File
from django.contrib					import messages
from django.conf					import settings
from django.shortcuts				import render, redirect
from .models						import CustomUser
from . 								import forms
from io								import BytesIO
import requests

# -----------------------Interactions avec le profil-------------------------- #

def login_or_register(request):
	login_form = AuthenticationForm()
	register_form = forms.CustomUserCreationForm()

	if request.method == 'POST':
		if 'login' in request.POST:
			login_form = AuthenticationForm(request, data=request.POST)
			if login_form.is_valid():
				username = login_form.cleaned_data.get('username')
				password = login_form.cleaned_data.get('password')
				user = authenticate(request, username=username, password=password)
				if user is not None:
					user.is_onsite = True
					user.save()
					login(request, user)
					messages.success(request, f'Welcome back, {user.username}!')
					return redirect('home:index')
				else:
					messages.error(request, 'Invalid username or password.')
			else:
				messages.error(request, 'Invalid username or password.')
		elif 'register' in request.POST:
			register_form = forms.CustomUserCreationForm(request.POST, request.FILES)
			if register_form.is_valid():
				user = register_form.save()
				login(request, user)
				return redirect("home:index")

	return render(request, 'user_manage/connexion.html', {
		'login_form': login_form,
		'register_form': register_form,
	})

@login_required
def logout_user(request):
	request.user.is_onsite = False
	request.user.save()
	logout(request)
	messages.success(request, 'You have been logged out successfully.')
	return redirect('home:index')

@login_required
def edit_user(request):
	user = request.user

	if request.method == 'POST':
		user_form = forms.CustomUserUpdateForm(request.POST, request.FILES, instance=user)
		if user_form.is_valid():
			user_form.save()
			return redirect("home:index")
	else:
		user_form = forms.CustomUserUpdateForm(instance=user)

	return render(request, 'user_manage/edit.html', {
		'user_form': user_form,
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

def profile(request, username):
	user = CustomUser.objects.get(username=username)
	return render(request, 'user_manage/profile.html', {
		'user': user,
	})

# ----------------------------------Social------------------------------------ #

def search(request):
	query = request.GET.get('query')
	if query:
		try:
			user = CustomUser.objects.get(username=query)
			return redirect('user_manage:profile', username=user.username)
		except CustomUser.DoesNotExist:
			messages.error(request, 'Profil non trouvé')
			return redirect('home:index')
	else:
		messages.error(request, 'Veuillez entrer un pseudonyme pour la recherche.')
		return redirect('home:index')

@login_required
def add_friend(request, friend):
	friend_add = CustomUser.objects.get(username=friend)
	try:
		request.user.friends.add(friend_add)
		if friend_add in request.user.blockeds.all():
			request.user.blockeds.remove(friend_add)
		messages.success(request, f'{friend_add.username} a été ajouté à votre liste d\'amis.')
	except CustomUser.DoesNotExist:
		messages.error(request, 'Cet utilisateur n\'existe pas.')
	return redirect('user_manage:profile', friend_add.username)

@login_required
def remove_friend(request, username):
	try:
		friend = CustomUser.objects.get(username=username)
		request.user.friends.remove(friend)
		messages.success(request, f'{friend.username} a été retiré de votre liste d\'amis.')
	except CustomUser.DoesNotExist:
		messages.error(request, 'Cet utilisateur n\'existe pas.')
	return redirect('user_manage:profile', friend.username)

def	block_user(request, username):
	block_usr = CustomUser.objects.get(username=username)
	try:
		request.user.blockeds.add(block_usr)
		if block_usr in request.user.friends.all():
			request.user.friends.remove(block_usr)
		messages.success(request, f'{block_usr.username} a été bloqué.')
	except CustomUser.DoesNotExist:
		messages.error(request, 'Cet utilisateur n\'existe pas.')
	return redirect('user_manage:profile', block_usr.username)

def unblock_user(request, username):
	try:
		friend = CustomUser.objects.get(username=username)
		request.user.blockeds.remove(friend)
		messages.success(request, f'{friend.username} a été retiré des utilisateurs bloqués.')
	except CustomUser.DoesNotExist:
		messages.error(request, 'Cet utilisateur n\'existe pas.')
	return redirect('user_manage:profile', friend.username)


# ----------------------------------API 42------------------------------------ #

def api_42_login(request):
	client_id = settings.CLIENT_ID_42
	redirect_uri = request.build_absolute_uri('/accounts/api_42_callback/')
	return redirect(f'https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code')

def api_42_callback(request):
	try:
		code = request.GET.get('code')
		client_id = settings.CLIENT_ID_42
		client_secret = settings.CLIENT_SECRET_42
		redirect_uri = request.build_absolute_uri('/accounts/api_42_callback/')

		token_response = requests.post('https://api.intra.42.fr/oauth/token', data={
			'grant_type': 'authorization_code',
			'client_id': client_id,
			'client_secret': client_secret,
			'code': code,
			'redirect_uri': redirect_uri,
		}).json()

		access_token = token_response.get('access_token')

		user_response = requests.get('https://api.intra.42.fr/v2/me', headers={
			'Authorization': f'Bearer {access_token}',
		}).json()
		username = user_response['login']
		email = user_response['email']
		first_name = user_response.get('first_name')
		last_name = user_response.get('last_name')
		image_url = user_response['image']['link']
		user, created = CustomUser.objects.get_or_create(username=username, defaults={
			'email': email,
			'first_name': first_name,
			'last_name': last_name,
			'is_onsite': True,
		})

		if not created:
			user.is_onsite = True
			user.save()

		if image_url:
			response = requests.get(image_url)
			response.raise_for_status()
			img_temp = BytesIO(response.content)
			user.avatar.save(f"{username}_avatar.jpg", File(img_temp), save=True)
		login(request, user)
		return redirect('home:index')

	except Exception as e:
		print(e)
		return redirect('user_manage:register')