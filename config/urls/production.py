from config.urls.base import urlpatterns, path, include

urlpatterns += path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
