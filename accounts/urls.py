from django.urls import path
from .views import UserListView, UserDetailView, SearchResultsListView, DashboardView, UserUpdateKYCView, UserStatusView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('user-status', UserStatusView.as_view(), name='check_user_status'),
    path('<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('update-kyc/<int:pk>', UserUpdateKYCView.as_view(), name='update_kyc'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('search/', SearchResultsListView.as_view(),
         name='search_results'),
]
