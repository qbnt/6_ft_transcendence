from django.urls	import path
from .				import views

app_name = "home"

urlpatterns = [
	path('', views.index, name='index'),
	path('partial', views.index_partial, name='index_partial'),
]
