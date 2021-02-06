from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path('', accounts_views.UserStatusView.as_view(), name='status'),
    # Profile Verification Routes
    path('profile/verification/option/', accounts_views.ProfileVerificationOptionView.as_view(),
         name='profile_verification_option'),
    path('profile/verification/sms/', accounts_views.ProfileVerificationSMSView.as_view(),
         name='profile_verification_sms'),
    path('profile/identity-proof/upload/', accounts_views.ProfileIdentityProofUploadView.as_view(),
         name='profile_identity_proof_upload'),
    # Profile Member Completion Routes
    path('profile/dashboard/', accounts_views.ProfileDashboardView.as_view(),
         name='dashboard'),
    path('profile/name/', accounts_views.ProfileNameView.as_view(),
         name='profile_name'),
    # Profile Master Completion Routes
    path('profile/apply/poolmaster/', accounts_views.ProfileApplyPoolmasterView.as_view(),
         name='profile_apply_poolmaster'),
    path('profile/detail/', accounts_views.ProfileDetailView.as_view(),
         name='profile_detail'),
    path('profile/picture/', accounts_views.ProfilePictureView.as_view(),
         name='profile_picture'),
    # Account Password Reset with OTP
    path('password/reset/otp/', accounts_views.AccountResetPasswordWithOTPView.as_view(),
         name='account_reset_password_with_otp'),
    path('password/reset/otp/confirm/', accounts_views.AccountResetPasswordWithOTPConfirmView.as_view(),
         name='account_reset_password_with_otp_confirm'),
    # Profile Billing Address & Transactions
    path('profile/billing-address/create/', accounts_views.ProfileBillingAddresssCreateView.as_view(),
         name='profile_billing_address_create'),
    path('profile/billing-address/update/<int:pk>/', accounts_views.ProfileBillingAddresssUpdateView.as_view(),
         name='profile_billing_address_update'),
    path('profile/balance-transaction/', accounts_views.ProfileBalanceTransactionListView.as_view(),
         name='profile_balance_transaction_list'),
    path('profile/investment-transaction/', accounts_views.ProfileInvestmentTransactionListView.as_view(),
         name='profile_investment_transaction_list'),
    # Profile Manager Specific Routes
    path('manager/profile/', accounts_views.ManagerProfileListView.as_view(),
         name='manager_profile_list'),
    path('manager/profile/<int:pk>/', accounts_views.ManagerProfileDetailView.as_view(),
         name='manager_profile_detail'),
    path('manager/profile/verify/identity/<int:pk>/', accounts_views.ManagerProfileVerifyIdentityView.as_view(),
         name='manager_profile_verify_identity'),
    path('manager/profile/approve/poolmaster/<int:pk>/', accounts_views.ManagerProfileApprovePoolmasterView.as_view(),
         name='manager_profile_approve_poolmaster'),
    path('manager/profile/search/', accounts_views.ManagerProfileSearchView.as_view(),
         name='manager_profile_search'),
]
