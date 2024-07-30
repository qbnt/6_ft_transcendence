from django.urls	import path
from .				import views

app_name = "user_manage"

urlpatterns = [
    path ('login/', views.login_user, name = 'login'),
	path ('logout/', views.logout_user, name = 'logout'),
	path ('register/', views.register_user, name = 'register'),
	path ('detail/', views.detail_user, name='detail'),
	path ('edit/', views.edit_user, name = 'edit'),
	path ('edit/pw_update/', views.pw_update, name = 'pw_update'),
]