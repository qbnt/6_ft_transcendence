# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from PIL import Image, ImageOps
from django.core.files import File
from io import BytesIO

class CustomUserManager(BaseUserManager):
	def create_user(self, username, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The Email field must be set')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(unique=True, max_length=42)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	avatar = models.ImageField(default='default_avatar.jpg', upload_to='profile_avatars')
	is_onsite = models.BooleanField(default=True)

	friends_request = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='users_requested')
	friends = models.ManyToManyField('self', blank=True, related_name='friend_with')
	blockeds = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='blocked_by')

	win_count = models.IntegerField(default=0)
	lose_count = models.IntegerField(default=0)
	is_ingame = models.BooleanField(default=False)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	a2f = models.BooleanField(default=False)
	a2f_code = models.IntegerField(default=0);

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.avatar.path)
		if img.height > 150 or img.width > 150:
			img = ImageOps.fit(img, (150, 150))
			img.save(self.avatar.path)