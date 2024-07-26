from django.urls	import path
from .				import views

urlpatterns = [
    path('', views.usr_list, name='usr_list'),
    path('usr_view/', views.usr_view, name='usr_view'),
    path('usr_create/', views.usr_create, name='usr_create'),
    path('usr_edit/', views.usr_edit, name='usr_edit'),
    path('usr_suppr/', views.usr_suppr, name='usr_suppr'),
    path('usr_connect/', views.usr_connect, name='usr_connect'),
]