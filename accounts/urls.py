from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path('', accounts_views.UserStatusView.as_view(), name='status'),
    path('contact/option', accounts_views.UserContactConfirmOptionView.as_view(),
         name='contact_confirmation_option'),
    path('contact/sms/confirm', accounts_views.UserContactSMSConfirmView.as_view(),
         name='contact_sms_confirm'),
    path('identity-proof-upload', accounts_views.UserIdentityProofUploadView.as_view(),
         name='identity_proof_upload'),
    path('dashboard/', accounts_views.DashboardView.as_view(), name='dashboard'),
    # TODO-URGENT: Update Profile Name (including name fields only)
    path('profile/name', accounts_views.UserProfileNameUpdateView.as_view(),
         name='profile_name'),
    # TODO-URGENT: Update Profile Details (including all fields)
    path('profile/datail', accounts_views.UserProfileDetailUpdateView.as_view(),
         name='profile_detail'),
    path('profile/picture', accounts_views.UserProfilePictureUploadView.as_view(),
         name='profile_picture'),

    path('users/', accounts_views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>', accounts_views.UserDetailView.as_view(), name='user_detail'),

    path('search/', accounts_views.SearchResultsListView.as_view(),
         name='user_search_results'),
]
