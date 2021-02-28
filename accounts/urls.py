from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path('', accounts_views.UserStatusView.as_view(), name='status'),
    # Profile Verification Routes
    path('profile/verification/option/', accounts_views.ProfileVerificationOptionView.as_view(),
         name='profile_verification_option'),
    path('profile/verification/sms/', accounts_views.ProfileVerificationSMSView.as_view(), name='profile_verification_sms'),
    path('profile/identity-proof/upload/', accounts_views.ProfileIdentityProofUploadView.as_view(),
         name='profile_identity_proof_upload'),
    # Profile Member Completion Routes
    path('profile/dashboard/', accounts_views.ProfileDashboardView.as_view(), name='dashboard'),
    path('profile/name/', accounts_views.ProfileNameView.as_view(), name='profile_name'),
    # Profile Master Completion Routes
    path('profile/apply/poolmaster/', accounts_views.ProfileApplyPoolmasterView.as_view(), name='profile_apply_poolmaster'),
    path('profile/detail/', accounts_views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/picture/', accounts_views.ProfilePictureView.as_view(), name='profile_picture'),
    # Account Password Reset with OTP
    path('password/reset/otp/', accounts_views.AccountResetPasswordWithOTPView.as_view(),
         name='account_reset_password_with_otp'),
    path('password/reset/otp/confirm/', accounts_views.AccountResetPasswordWithOTPConfirmView.as_view(),
         name='account_reset_password_with_otp_confirm'),
    # Profile Billing Address, Bank Account Detail & Transactions
    path('profile/billing-address/create/', accounts_views.ProfileBillingAddresssCreateView.as_view(),
         name='profile_billing_address_create'),
    path('profile/billing-address/update/<int:pk>/',
         accounts_views.ProfileBillingAddresssUpdateView.as_view(), name='profile_billing_address_update'),
    path('profile/bank-account-detail/create/', accounts_views.ProfileBankAccountDetailCreateView.as_view(),
         name='profile_bank_account_detail_create'),
    path('profile/bank-account-detail/update/<int:pk>/',
         accounts_views.ProfileBankAccountDetailUpdateView.as_view(), name='profile_bank_account_detail_update'),
    path('profile/balance-transaction/', accounts_views.ProfileBalanceTransactionListView.as_view(),
         name='profile_balance_transaction_list'),
    path('profile/investment-transaction/', accounts_views.ProfileInvestmentTransactionListView.as_view(),
         name='profile_investment_transaction_list'),
    # Profile Credit, Debit Balance
    path('profile/balance/credit/', accounts_views.ProfileCreditBalanceView.as_view(),
         name='profile_balance_credit_transaction_create'),
    path('profile/balance/credit/confirm/<int:pk>/', accounts_views.ProfileCreditBalanceConfirmView.as_view(),
         name='profile_balance_transaction_confirm'),
    path('profile/balance/credit/status/<int:pk>/', accounts_views.ProfileCreditBalanceStatusView.as_view(),
         name='profile_balance_transaction_status'),
    path('profile/balance/debit/', accounts_views.ProfileCreditBalanceView.as_view(),
         name='profile_balance_debit_transaction_create'),
    # Support Ticket Specific Routes
    path('profile/support-ticket/create', accounts_views.ProfileSupportTicketCreateView.as_view(),
         name='profile_support_ticket_create'),
    path('profile/support-ticket/update/<int:pk>/',
         accounts_views.ProfileSupportTicketUpdateView.as_view(), name='profile_support_ticket_update'),
    path('profile/support-ticket/all', accounts_views.ProfileSupportTicketListView.as_view(), name='profile_support_ticket_list'),
    # Profile Manager Specific Routes
    path('manager/profile/all/', accounts_views.ManagerProfileListView.as_view(), name='manager_profile_list'),
    path('manager/profile/member/', accounts_views.ManagerProfileListPoolMemberView.as_view(),
         name='manager_profile_member_list'),
    path('manager/profile/master/', accounts_views.ManagerProfileListPoolMasterView.as_view(),
         name='manager_profile_master_list'),
    path('manager/profile/willing/master/', accounts_views.ManagerProfileListWillingPoolMasterView.as_view(),
         name='manager_profile_willing_master_list'),
    path('manager/profile/unverified/', accounts_views.ManagerProfileListUnverifiedProfileView.as_view(),
         name='manager_profile_unverified_list'),
    path('manager/profile/<int:pk>/', accounts_views.ManagerProfileDetailView.as_view(), name='manager_profile_detail'),
    path('manager/profile/verify/identity/<int:pk>/',
         accounts_views.ManagerProfileVerifyIdentityView.as_view(), name='manager_profile_verify_identity'),
    path('manager/profile/approve/poolmaster/<int:pk>/',
         accounts_views.ManagerProfileApprovePoolmasterView.as_view(), name='manager_profile_approve_poolmaster'),
    path('manager/profile/search/', accounts_views.ManagerProfileSearchView.as_view(), name='manager_profile_search'),
    path('manage/pool/manage/', accounts_views.ManagerManagePoolView.as_view(), name='manager_manage_pool'),
    # List All Active Support Ticket
    # Update Active Ticket Details (Some Readonly Fields)
    path('manager/support-ticket/financial/', accounts_views.ManagerFinancialSupportTicketListView.as_view(),
         name='manager_financial_support_ticket_list'),
    path('manager/support-ticket/application/', accounts_views.ManagerApplicationSupportTicketListView.as_view(),
         name='manager_application_support_ticket_list'),
    path('manager/support-ticket/update/<int:pk>/',
         accounts_views.ManagerSupportTicketUpdateView.as_view(), name='manager_support_ticket_update'),
]
