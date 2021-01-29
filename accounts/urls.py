from django.urls import path
from .views import UserListView, UserDetailView, SearchResultsListView, DashboardView, UserUpdateProfileView, UserStatusView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>', UserUpdateProfileView.as_view(), name='user_profile'),
    path('kyc/<int:pk>', UserUpdateProfileView.as_view(), name='user_kyc'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('search/', SearchResultsListView.as_view(),
         name='search_results'),
    path('user-status', UserStatusView.as_view(), name='check_user_status'),
]
