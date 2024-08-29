from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
	path('<username>', views.get_or_create_chatroom, name='start_chat'),
	path('room/<chatroom_name>', views.chat_view, name='chatroom'),
	path('check_chat_rooms/', views.check_chat_rooms, name='check_chat_rooms'),
]