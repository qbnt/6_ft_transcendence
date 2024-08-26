from django			import forms
from .models		import GroupMessage

from django import forms
from .models import GroupMessage

class ChatmessageCreateForm(forms.ModelForm):
	class Meta:
		model = GroupMessage
		fields = ['body']
		labels = {
			'body': '',
		}
		widgets = {
			'body': forms.TextInput(attrs={
				'placeholder': 'Add message ...',
				'maxlength': '300',
				'autofocus': True,
				'class': 'form-control'
			}),
		}