from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import CustomUser


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'account/user_list.html'
    login_url = 'account_login'


class UserDetailView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'account/user_detail.html'
    login_url = 'account_login'


class SearchResultsListView(ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'account/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return CustomUser.objects.filter(
            Q(email__icontains=query) | Q(first_name__icontains=query) |
            Q(last_name__icontains=query) | Q(username__icontains=query)
        )
