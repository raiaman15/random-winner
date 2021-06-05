from config.urls.base import urlpatterns
from config.settings import base
from django.conf.urls.static import static

urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
