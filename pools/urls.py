from django.urls import path
from .views import PoolCreateView, PoolListView, PoolDetailView, SearchResultsListView

urlpatterns = [
    path('create', PoolCreateView.as_view(), name='pool_create'),
    path('', PoolListView.as_view(), name='pool_list'),
    path('<int:pk>', PoolDetailView.as_view(), name='pool_detail'),
    path('search', SearchResultsListView.as_view(),
         name='pool_search_results'),
]
