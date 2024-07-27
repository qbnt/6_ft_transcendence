from django.urls	import path
from .				import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('add/', views.user_add, name='user_add'),
    # path('usr_edit/', views.usr_edit, name='usr_edit'),
    # path('usr_suppr/', views.usr_suppr, name='usr_suppr'),
    # path('usr_connect/', views.usr_connect, name='usr_connect'),
]