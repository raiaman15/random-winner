from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.PoolCreateView.as_view(), name='pool_create'),
    path('all/', views.PoolListView.as_view(), name='pool_list'),
    path('membership/', views.PoolMembershipListView.as_view(), name='pool_membership_list'),
    path('mastership/', views.PoolMastershipListView.as_view(), name='pool_mastership_list'),
    path('detail/<int:pk>/', views.PoolDetailView.as_view(), name='pool_detail'),
    path('search/', views.PoolSearchView.as_view(), name='pool_search_results'),

    path('invite/create/', views.PoolInviteCreateView.as_view(), name='pool_invite_create'),
    path('invite/', views.PoolInviteListView.as_view(), name='pool_invite_list'),

    path('join/', views.PoolJoinView.as_view(), name='pool_join'),
    path('p9k4u2h3t6f0e8s/', views.AutomaticActivateScheduleView.as_view(), name='automatic_activate_pool'),
    path('z2s2c7f8b7h5m3k1e2c3t1b3y1m/', views.AutomaticSpinScheduleView.as_view(), name='automatic_spin_pool'),
]
