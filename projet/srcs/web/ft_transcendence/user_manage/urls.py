from django.urls	import path
from .				import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('add/', views.user_add, name='user_add'),
    path('edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('delete/<int:user_id>', views.user_delete, name='user_delete'),
    # path('usr_connect/', views.usr_connect, name='usr_connect'),
]