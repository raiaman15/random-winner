from config.urls.base import urlpatterns, path, include

# Enable 2FA for Admin (Device Authentication)
# from django_otp.admin import OTPAdminSite
# admin.site.__class__ = OTPAdminSite

urlpatterns += path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
