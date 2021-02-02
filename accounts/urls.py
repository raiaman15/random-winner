from django.urls import path
from .views import UserListView, UserDetailView, UserProfileView, UserIdentityProofUploadView, UserContactView, UserContactConfirmView, SearchResultsListView, DashboardView, UserStatusView

urlpatterns = [
    path('', UserStatusView.as_view(), name='status'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('identity-proof-upload', UserIdentityProofUploadView.as_view(),
         name='identity_proof_upload'),
    path('contact', UserContactView.as_view(), name='contact'),
    path('contact/verify', UserContactConfirmView.as_view(),
         name='contact_confirm'),
    path('search/', SearchResultsListView.as_view(), name='user_search_results'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
