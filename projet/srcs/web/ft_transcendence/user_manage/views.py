from django.shortcuts	import render, get_object_or_404, redirect
from django.contrib 	import messages
from .models			import User
from .forms				import UserForm


def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user_manage/usr_list.html', context)

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {'user': user}
    return render(request, 'user_manage/usr_detail.html', context)

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

def usr_edit(request):
	pass

def usr_suppr(request):
	pass

def usr_connect(request):
	pass