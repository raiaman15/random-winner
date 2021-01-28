from django.urls import path
from .views import PoolListView, PoolDetailView, SearchResultsListView  # new

urlpatterns = [
    path('', PoolListView.as_view(), name='book_list'),
    path('<uuid:pk>', PoolDetailView.as_view(), name='book_detail'),
    path('search/', SearchResultsListView.as_view(),
         name='search_results'),  # new
]
