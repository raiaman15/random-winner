from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path('', accounts_views.UserStatusView.as_view(), name='status'),
    # Profile Verification Routes
    path('profile/verification/option', accounts_views.UserContactConfirmOptionView.as_view(),
         name='profile_verification_option'),
    path('profile/verification/sms', accounts_views.UserContactSMSConfirmView.as_view(),
         name='profile_verification_sms'),
    path('profile/identity-proof/upload', accounts_views.UserIdentityProofUploadView.as_view(),
         name='profile_identity_proof_upload'),
    # Profile Member Completion Routes
    path('dashboard/', accounts_views.DashboardView.as_view(), name='dashboard'),
    path('profile/name', accounts_views.UserProfileNameUpdateView.as_view(),
         name='profile_name'),
    # Profile Master Completion Routes
    path('profile/apply/poolmaster', accounts_views.UserPoolMasterApplicationView.as_view(),
         name='profile_apply_postmaster'),
    path('profile/datail', accounts_views.UserProfileDetailUpdateView.as_view(),
         name='profile_detail'),
    path('profile/picture', accounts_views.UserProfilePictureUploadView.as_view(),
         name='profile_picture'),
    # Profile Manager Specific Routes
    path('profile/', accounts_views.UserListView.as_view(), name='profile_list'),
    path('profile/<int:pk>', accounts_views.UserDetailView.as_view(),
         name='profile_detail'),
    path('profile/search', accounts_views.SearchResultsListView.as_view(),
         name='profile_search'),
]
