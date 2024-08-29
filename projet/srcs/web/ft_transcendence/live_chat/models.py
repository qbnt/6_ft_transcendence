from django.db			import models
from user_manage.models	import CustomUser
import shortuuid

class OnlineUsers(models.Model):
	users_online = models.ManyToManyField(CustomUser, related_name='onsite', blank=True)

	def __str__(self):
		return f"{self.users_online.count()} utilisateurs en ligne"

class	ChatGroup(models.Model):
	group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
	users_online = models.ManyToManyField(CustomUser, related_name='online_in_groups', blank=True)
	members = models.ManyToManyField(CustomUser, related_name='chat_groups', blank=True)
	is_private = models.BooleanField(default=False)

	def __str__(self):
		return self.group_name

class	GroupMessage(models.Model):
	group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	body = models.CharField(max_length=300, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return f'{self.author.username} : {self.body}'

	class Meta:
		ordering = ['-created']