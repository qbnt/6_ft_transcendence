from django.db						import models
from django.contrib.auth.hashers	import make_password, check_password

class User(models.Model):
	username	= models.CharField(max_length=150, unique=True)
	password	= models.CharField(max_length=128)
	email		= models.EmailField(unique=True)
	date_joined	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.username

	def set_password(self, raw_pw):
		self.password = make_password(raw_pw)
		self.save()

	def check_password(self, raw_pw):
		return check_password(raw_pw, self.password)