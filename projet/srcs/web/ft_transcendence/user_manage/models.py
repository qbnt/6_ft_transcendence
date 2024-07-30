from django.db					import models
from django.contrib.auth.models	import User
from PIL						import Image, ImageOps
from django.db.models.signals	import post_delete
from django.dispatch			import receiver


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='default_avatar.jpg', upload_to='profile_avatars')
	win_count = models.IntegerField(default=0)
	lose_count = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.avatar.path)
		if img.height > 300 or img.width > 300:
			img = ImageOps.fit(img, (300, 300))
			img.save(self.avatar.path)


@receiver(post_delete, sender=Profile)
def delete_user_with_profile(sender, instance, **kwargs):
    user = instance.user
    if user and user.id:
        user.delete()