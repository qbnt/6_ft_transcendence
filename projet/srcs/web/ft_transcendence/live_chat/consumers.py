from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.shortcuts 			import get_object_or_404
from django.template.loader 	import render_to_string
from channels.db				import database_sync_to_async
from asgiref.sync 				import async_to_sync
import json
from .models 					import *

class OnlineStatusConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		user = self.scope['user']
		if user.is_authenticated:
			await self.add_user_online(user)
			await self.channel_layer.group_add("online_users", self.channel_name)
			await self.accept()

	async def disconnect(self, close_code):
		user = self.scope['user']
		if user.is_authenticated:
			await self.remove_user_online(user)
			await self.channel_layer.group_discard("online_users", self.channel_name)

	async def receive(self, text_data=None, bytes_data=None):
		# Optionnel : si vous voulez gérer les messages entrants
		pass

	@database_sync_to_async
	def add_user_online(self, user):
		online_users, _ = OnlineUsers.objects.get_or_create(pk=1)
		online_users.users_online.add(user)

	@database_sync_to_async
	def remove_user_online(self, user):
		online_users, _ = OnlineUsers.objects.get_or_create(pk=1)
		online_users.users_online.remove(user)

class ChatroomConsumer(WebsocketConsumer):
	def connect(self):
		self.user = self.scope['user']
		self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
		self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

		async_to_sync(self.channel_layer.group_add)(
			self.chatroom_name, self.channel_name
		)

		if self.user not in self.chatroom.users_online.all():
			self.chatroom.users_online.add(self.user)
			self.update_online_count()

		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.chatroom_name, self.channel_name
		)

		if self.user in self.chatroom.users_online.all():
			self.chatroom.users_online.remove(self.user)
			self.update_online_count()

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		body = text_data_json['body']

		message = GroupMessage.objects.create(
			body = body,
			author = self.user,
			group = self.chatroom
		)
		event = {
			'type': 'message_handler',
			'message_id': message.id,
		}
		async_to_sync(self.channel_layer.group_send)(
			self.chatroom_name, event
		)

	def message_handler(self, event):
		message_id = event['message_id']
		message = GroupMessage.objects.get(id=message_id)
		context = {
			'message': message,
			'user': self.user,
		}
		html = render_to_string("live_chat/partials/chat_message_p.html", context=context)
		self.send(text_data=html)

	def update_online_count(self):
		online_count = self.chatroom.users_online.count() - 1

		event = {
			'type': 'online_count_handler',
			'online_count': online_count,
		}
		async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

	def online_count_handler(self, event):
		online_count = event['online_count']
		html = render_to_string("live_chat/partials/online_count.html", {'online_count': online_count})
		self.send(text_data=html)
