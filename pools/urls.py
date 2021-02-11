from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.PoolCreateView.as_view(), name='pool_create'),
    path('all/', views.PoolListView.as_view(), name='pool_list'),
    path('membership/', views.PoolMembershipListView.as_view(), name='pool_membership_list'),
    path('mastership/', views.PoolMastershipListView.as_view(), name='pool_mastership_list'),
    path('detail/<int:pk>/', views.PoolDetailView.as_view(), name='pool_detail'),
    path('search/', views.PoolSearchView.as_view(),
         name='pool_search_results'),

    path('invite/create/', views.PoolInviteCreateView.as_view(), name='pool_invite_create'),
    path('invite/', views.PoolInviteListView.as_view(), name='pool_invite_list'),

    path('join/', views.PoolJoinView.as_view(), name='pool_join'),
]
