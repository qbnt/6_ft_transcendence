from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserUpdateForm, CustomUserCreationForm, AddFriendForm
from .models import CustomUser

# -------------------------Creation et connections---------------------------- #

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home:index")
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect.")

    form = AuthenticationForm()
    return render(request, "user_manage/login.html", {'form': form})

def logout_user(request):
    logout(request)
    return redirect("home:index")

def register_user(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)  # Connexion de l'utilisateur après l'enregistrement
            return redirect("home:index")
    else:
        user_form = CustomUserCreationForm()

    return render(request, "user_manage/register.html", {
        'user_form': user_form,
    })

@login_required
def profile(request):
    return render(request, 'user_manage/detail.html', {'user': request.user})

# ------------------------------Edition--------------------------------------- #

@login_required
def edit_user(request):
    user = request.user

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect("home:index")
    else:
        user_form = CustomUserUpdateForm(instance=user)

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

# ------------------------------Social---------------------------------------- #

@login_required
def add_friend(request):
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            try:
                friend = CustomUser.objects.get(username=form.cleaned_data['username'])
                request.user.friends.add(friend)
                messages.success(request, f'{friend.username} a été ajouté à votre liste d\'amis.')
                return redirect('user_manage:profile')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Cet utilisateur n\'existe pas.')
    else:
        form = AddFriendForm()

    return render(request, 'user_manage/add_friend.html', {'form': form})

@login_required
def remove_friend(request, username):
    try:
        friend = CustomUser.objects.get(username=username)
        request.user.friends.remove(friend)
        messages.success(request, f'{friend.username} a été retiré de votre liste d\'amis.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Cet utilisateur n\'existe pas.')
    return redirect('user_manage:profile')
