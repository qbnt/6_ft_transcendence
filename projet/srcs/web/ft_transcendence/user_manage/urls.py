from django.urls	import path
from .				import views

app_name = "user_manage"

urlpatterns = [
	path ('connexion/', views.login_or_register, name='connexion'),
	path ('logout/', views.logout_user, name = 'logout'),
	path ('edit/', views.edit_user, name = 'edit'),
	path ('edit/pw_update/', views.pw_update, name = 'pw_update'),
	path ('edit/a2f/', views.a2f, name = 'a2f'),
	path ('edit/a2f/send_mail', views.send_email, name = 'a2f_send_mail'),
	path ('profile/<str:username>', views.profile, name='profile'),

	path ('search/', views.search, name='search'),
	path ('add_friend/<str:friend>', views.add_friend, name='add_friend'),
	path ('accept_friend/<str:friend>', views.accept_friend, name='accept_friend'),
	path ('refuse_friend/<str:friend>', views.refuse_friend, name='refuse_friend'),
	path ('remove_friend_request/<str:friend>', views.remove_friend_request, name='remove_friend_request'),
	path ('remove_friend/<str:username>/', views.remove_friend, name='remove_friend'),
	path ('block_user/<str:username>/', views.block_user, name='block'),
	path ('unblock_user/<str:username>/', views.unblock_user, name='unblock'),

	path ('api_42_login/', views.api_42_login, name='api_42_login'),
	path ('api_42_callback/', views.api_42_callback, name='api_42_callback'),
]