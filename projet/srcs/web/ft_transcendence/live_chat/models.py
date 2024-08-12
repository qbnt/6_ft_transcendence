from django.db			import models
from user_manage.models	import CustomUser

class	ChatGroup(models.Model):
	group_name = models.CharField(max_length=128, unique=True, blank=True)
	users_online = models.ManyToManyField(CustomUser, related_name='online_in_groups', blank=True)

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