from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path('', accounts_views.UserStatusView.as_view(), name='status'),
    # Profile Verification Routes
    path('profile/verification/option', accounts_views.ProfileVerificationOptionView.as_view(),
         name='profile_verification_option'),
    path('profile/verification/sms', accounts_views.ProfileVerificationSMSView.as_view(),
         name='profile_verification_sms'),
    path('profile/identity-proof/upload', accounts_views.ProfileIdentityProofUploadView.as_view(),
         name='profile_identity_proof_upload'),
    # Profile Member Completion Routes
    path('profile/dashboard', accounts_views.ProfileDashboardView.as_view(),
         name='dashboard'),
    path('profile/name', accounts_views.ProfileNameView.as_view(),
         name='profile_name'),
    # Profile Master Completion Routes
    path('profile/apply/poolmaster', accounts_views.ProfileApplyPoolmasterView.as_view(),
         name='profile_apply_postmaster'),
    path('profile/detail', accounts_views.ProfileDetailView.as_view(),
         name='profile_detail'),
    path('profile/picture', accounts_views.ProfilePictureView.as_view(),
         name='profile_picture'),
    # Profile Manager Specific Routes
    path('profile/', accounts_views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>', accounts_views.ProfileDetailView.as_view(),
         name='profile_detail'),
    path('profile/search', accounts_views.ProfileSearchView.as_view(),
         name='profile_search'),
]
