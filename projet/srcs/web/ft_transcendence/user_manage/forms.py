from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# ---------------------- Formulaires de création et de modification d'utilisateur ---------------------- #

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(
		required=True,
		help_text="Un email valide est requis."
	)
	first_name = forms.CharField(
		max_length=30,
		required=False,
		help_text="Optionnel."
	)
	last_name = forms.CharField(
		max_length=30,
		required=False,
		help_text="Optionnel."
	)
	avatar = forms.ImageField(required=False)
	win_count = forms.IntegerField(
		required=False,
		initial=0,
		widget=forms.HiddenInput()
	)
	lose_count = forms.IntegerField(
		required=False,
		initial=0,
		widget=forms.HiddenInput()
	)

	class Meta:
		model = CustomUser
		fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'password1', 'password2')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if CustomUser.objects.filter(email=email).exists():
			raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
		return email

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user

class CustomUserUpdateForm(forms.ModelForm):
	current_password = forms.CharField(
		label="Mot de passe actuel",
		widget=forms.PasswordInput,
		required=True,
		help_text="Entrez votre mot de passe actuel pour confirmer les modifications."
	)
	avatar = forms.ImageField(required=False)

	class Meta:
		model = CustomUser
		fields = ['username', 'first_name', 'last_name', 'email', 'avatar']

	def clean_current_password(self):
		current_password = self.cleaned_data['current_password']
		user = authenticate(username=self.instance.username, password=current_password)
		if user is None:
			raise forms.ValidationError("Le mot de passe actuel est incorrect.")
		return current_password
	
class A2F(forms.Form):
    code_client = forms.CharField(label="Code A2F", max_length=6, required=True)