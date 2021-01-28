from django.urls import path
from .views import UserListView, UserDetailView, SearchResultsListView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<uuid:pk>', UserDetailView.as_view(), name='user_detail'),
    path('search/', SearchResultsListView.as_view(),
         name='search_results'),
]
