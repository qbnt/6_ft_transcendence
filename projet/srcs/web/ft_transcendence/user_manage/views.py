from django.shortcuts	import render, get_object_or_404, redirect
from django.contrib 	import messages
from .models			import User
from .forms				import UserForm


def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user_manage/usr_list.html', context)

def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Utilisateur ajouté avec succès!')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_manage/usr_add.html', {'form': form})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {'user': user}
    return render(request, 'user_manage/usr_detail.html', context)

def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Utilisateur mis à jour avec succès!')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_manage/usr_edit.html', {'form': form, 'user': user})

def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Utilisateur supprimé avec succès!')
        return redirect('user_list')
    return render(request, 'user_manage/usr_delete.html', {'user': user})

def usr_connect(request):
	pass