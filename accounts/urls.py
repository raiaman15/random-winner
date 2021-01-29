from django.urls import path
from .views import UserListView, UserDetailView, UserUpdateProfileView, UserUpdateIdentityView, UserUpdatePhoneView, UserStatusView, SearchResultsListView, DashboardView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile', UserUpdateProfileView.as_view(), name='profile'),
    path('identity', UserUpdateIdentityView.as_view(), name='identity'),
    path('contact', UserUpdatePhoneView.as_view(), name='contact'),
    path('contact/verify', UserUpdatePhoneView.as_view(),
         name='contact_verify'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('search/', SearchResultsListView.as_view(),
         name='search_results'),
    path('status', UserStatusView.as_view(), name='status'),
]
