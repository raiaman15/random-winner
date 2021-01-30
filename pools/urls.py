from django.urls import path
from .views import PoolListView, PoolDetailView, SearchResultsListView  # new

urlpatterns = [
    path('pools/', PoolListView.as_view(), name='pool_list'),
    path('pools/<int:pk>', PoolDetailView.as_view(), name='pool_detail'),
    path('search/', SearchResultsListView.as_view(),
         name='pool_search_results'),
]
