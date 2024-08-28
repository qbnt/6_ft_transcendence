from django.contrib.auth			import authenticate, login, logout
from django.contrib.auth.forms		import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators	import login_required
from django.core.files 				import File
from django.contrib					import messages
from django.conf					import settings
from django.shortcuts				import render, redirect
from .models						import CustomUser
from live_chat.models				import OnlineUsers
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
					user.save()
					login(request, user)
					messages.success(request, f'Content de te revoir, {user.username} !')
					return redirect('home:index')
				else:
					messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
			else:
				messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
		elif 'register' in request.POST:
			register_form = forms.CustomUserCreationForm(request.POST, request.FILES)
			if register_form.is_valid():
				user = register_form.save()
				login(request, user)
				messages.success(request, 'Inscription réussie ! Bienvenue !')
				return redirect("home:index")
			else:
				for error in register_form.errors.values():
					messages.error(request, error)

	return render(request, 'user_manage/connexion.html', {
		'login_form': login_form,
		'register_form': register_form,
	})

def profile(request, username):
	user = CustomUser.objects.get(username=username)
	online = OnlineUsers.objects.first()
	return render(request, 'user_manage/profile.html', {
		'user': user,
		'online': online
	})

@login_required
def logout_user(request):
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
			messages.success(request, f'Vos modifications ont bien étaient enregistrés {user.username}!')
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
		if request.user in friend_add.blockeds.all():
			messages.error(request, 'Cet utilisateur vous a bloqué.')
		else:
			friend_add.friends_request.add(request.user)
			if friend_add in request.user.blockeds.all():
				request.user.blockeds.remove(friend_add)
				messages.success(request, f'{friend_add.username} a été retiré de vos utilisateurs bloqués.')
			messages.success(request, f'{friend_add.username} a reçu une demande d\'ami.')
	except CustomUser.DoesNotExist:
		messages.error(request, 'Cet utilisateur n\'existe pas.')
	return redirect('user_manage:profile', friend_add.username)

@login_required
def accept_friend(request, friend):
	friend_request = CustomUser.objects.get(username=friend)
	if friend_request in request.user.friends_request.all():
		request.user.friends_request.remove(friend_request)
		request.user.friends.add(friend_request)
		friend_request.friends.add(request.user)
		messages.success(request, f'Vous êtes maintenant ami avec {friend_request.username}.')
	else:
		messages.error(request, 'Cette demande d\'ami n\'existe pas.')
	return redirect('user_manage:profile', username=request.user.username)

@login_required
def refuse_friend(request, friend):
	friend_request = CustomUser.objects.get(username=friend)
	if friend_request in request.user.friends_request.all():
		request.user.friends_request.remove(friend_request)
		messages.success(request, f'La demande d\'ami de {friend_request.username} a été refusée.')
	else:
		messages.error(request, 'Cette demande d\'ami n\'existe pas.')
	return redirect('user_manage:profile', username=request.user.username)

@login_required
def	remove_friend_request(request, friend):
	friend_request = CustomUser.objects.get(username=friend)
	request.user.users_requested.remove(friend_request)
	messages.success(request, f'La demande d\'ami pour {friend_request.username} a bien été supprimée.')
	return redirect('user_manage:profile', username=friend_request.username)

@login_required
def remove_friend(request, username):
	try:
		friend = CustomUser.objects.get(username=username)
		request.user.friends.remove(friend)
		messages.success(request, f'{friend.username} a été retiré de votre liste d\'amis.')
	except CustomUser.DoesNotExist:
		messages.error(request, 'Cet utilisateur n\'existe pas.')
	return redirect('user_manage:profile', friend.username)

@login_required
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

@login_required
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
		user, created = CustomUser.objects.get_or_create(
			username=username, defaults={
				'email': email,
				'first_name': first_name,
				'last_name': last_name,
			}
		)

		if not created:
			messages.success(request, f'Welcome back, {user.username}!')
			user.save()
		else:
			messages.success(request, f'Welcome, {user.username}!')

		if image_url:
			response = requests.get(image_url)
			response.raise_for_status()
			img_temp = BytesIO(response.content)
			user.avatar.save(f"{username}_avatar.jpg", File(img_temp), save=True)
		login(request, user)
		return redirect('home:index')

	except Exception as e:
		messages.error(request, "Erreur lors de la communication avec les serveurs de 42.")
		return redirect('user_manage:connexion')

@login_required
def check_online_status(request):
	online_users = OnlineUsers.objects.first()
	return render(request, 'partial/friend_list_partial.html', {'online_users': online_users})