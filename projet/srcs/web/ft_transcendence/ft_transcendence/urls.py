from django.contrib				import admin
from django.urls 				import path, include
from django.conf				import settings
from django.conf.urls.static	import static

urlpatterns = [
    path('', include('django_prometheus.urls')),
	path('', include('home.urls'), name='home'),
	path('pong/', include('pong_game.urls'), name='pong'),
	path('tournament/', include('tournament.urls'), name='tournament'),
	path('live-chat/', include('live_chat.urls'), name='chat'),
	path('accounts/', include('user_manage.urls'), name='accounts'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)