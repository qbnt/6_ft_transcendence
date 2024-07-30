from django						import forms
from django.contrib.auth		import authenticate
from django.contrib.auth.forms	import UserCreationForm
from django.contrib.auth.models	import User
from .models					import Profile

# ---------------------------------------------------------------------------- #

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Un email valide est requis.")
    first_name = forms.CharField(max_length=30, required=False, help_text="Optionnel.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optionnel.")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
        return email

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
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

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        user = authenticate(username=self.instance.username, password=current_password)
        if user is None:
            raise forms.ValidationError("Le mot de passe actuel est incorrect.")
        return current_password

# ---------------------------------------------------------------------------- #

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']