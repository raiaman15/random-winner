from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.PoolCreateView.as_view(), name='pool_create'),
    path('list/', views.PoolListView.as_view(), name='pool_list'),
    path('detail/<int:pk>/', views.PoolDetailView.as_view(), name='pool_detail'),
    path('search/', views.PoolSearchView.as_view(),
         name='pool_search_results'),

    path('invite/create/', views.PoolInviteCreateView.as_view(), name='pool_invite_create'),
    path('invite/list/', views.PoolInviteListView.as_view(), name='pool_invite_list'),
]
