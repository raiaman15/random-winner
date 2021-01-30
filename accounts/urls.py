from django.urls import path
from .views import UserListView, UserDetailView, UserProfileView, UserIdentityView, UserContactView, UserContactConfirmView, SearchResultsListView, DashboardView, UserStatusView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('identity', UserIdentityView.as_view(), name='identity'),
    path('contact', UserContactView.as_view(), name='contact'),
    path('contact/verify', UserContactConfirmView.as_view(),
         name='contact_confirm'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('search/', SearchResultsListView.as_view(),
         name='search_results'),
    path('status', UserStatusView.as_view(), name='status'),
]
