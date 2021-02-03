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
    # Account Password Reset with OTP
    path('password/reset/otp', accounts_views.AccountResetPasswordWithOTPView.as_view(),
         name='account_reset_password_with_otp'),
    # Profile Manager Specific Routes
    path('manager/profile/', accounts_views.ManagerProfileListView.as_view(),
         name='manager_profile_list'),
    path('manager/profile/<int:pk>', accounts_views.ManagerProfileDetailView.as_view(),
         name='manager_profile_detail'),
    path('manager/profile/search', accounts_views.ManagerProfileSearchView.as_view(),
         name='manager_profile_search'),
]
