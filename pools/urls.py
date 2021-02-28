from django.urls import path
from . import views as pools_views

urlpatterns = [
    path('create/', pools_views.PoolCreateView.as_view(), name='pool_create'),
    path('all/', pools_views.PoolListView.as_view(), name='pool_list'),
    path('membership/', pools_views.PoolMembershipListView.as_view(), name='pool_membership_list'),
    path('mastership/', pools_views.PoolMastershipListView.as_view(), name='pool_mastership_list'),
    path('detail/<int:pk>/', pools_views.PoolDetailView.as_view(), name='pool_detail'),
    path('search/', pools_views.PoolSearchView.as_view(), name='pool_search_results'),
    path('invite/create/', pools_views.PoolInviteCreateView.as_view(), name='pool_invite_create'),
    path('invite/', pools_views.PoolInviteListView.as_view(), name='pool_invite_list'),
    path('join/', pools_views.PoolJoinView.as_view(), name='pool_join'),
    # List All Manager Related Functionality
    path('HZR0N2B4PPUSLXLY9FWC/', pools_views.AutomaticActivateScheduleView.as_view(), name='automatic_activate_pool'),
    path('VIY8ZUGF7SIUI32DDBKP/', pools_views.AutomaticSpinScheduleView.as_view(), name='automatic_spin_pool'),
    path('4ANJ9575MZMOPCRVLWIK/', pools_views.PoolStatisticsView.as_view(), name='pool_statistics'),
]
