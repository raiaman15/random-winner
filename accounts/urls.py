from django.urls import path
from .views import UserListView, UserDetailView, UserUpdateProfileView, UserUpdateKYCView, UserUpdatePhoneView, UserStatusView, SearchResultsListView, DashboardView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile', UserUpdateProfileView.as_view(), name='profile'),
    path('kyc', UserUpdateKYCView.as_view(), name='kyc'),
    path('phone', UserUpdatePhoneView.as_view(), name='phone'),
    path('phone/verify', UserUpdatePhoneView.as_view(),
         name='phone_verify'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('search/', SearchResultsListView.as_view(),
         name='search_results'),
    path('status', UserStatusView.as_view(), name='user_status'),
]
