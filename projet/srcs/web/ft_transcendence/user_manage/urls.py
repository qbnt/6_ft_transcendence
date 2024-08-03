from django.urls	import path
from .				import views

app_name = "user_manage"

urlpatterns = [
    path ('login/', views.login_user, name = 'login'),
	path ('logout/', views.logout_user, name = 'logout'),
	path ('register/', views.register_user, name = 'register'),

	path ('profile/', views.profile, name='profile'),
	path ('edit/', views.edit_user, name = 'edit'),
	path ('edit/pw_update/', views.pw_update, name = 'pw_update'),

	path ('add_friend/', views.add_friend, name='add_friend'),
    path ('remove_friend/<str:username>/', views.remove_friend, name='remove_friend'),

	path ('api_42_login/', views.api_42_login, name='api_42_login'),
    path ('api_42_callback/', views.api_42_callback, name='api_42_callback'),
]