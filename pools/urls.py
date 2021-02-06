from django.urls import path
from .views import PoolCreateView, PoolListView, PoolDetailView, PoolSearchView

urlpatterns = [
    path('create/', PoolCreateView.as_view(), name='pool_create'),
    path('list/', PoolListView.as_view(), name='pool_list'),
    path('detail/<int:pk>/', PoolDetailView.as_view(), name='pool_detail'),
    path('search/', PoolSearchView.as_view(),
         name='pool_search_results'),
]
