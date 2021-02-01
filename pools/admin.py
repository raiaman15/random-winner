from django.contrib import admin
from .models import Pool, PoolMember, InvestmentTransaction


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('codename', 'name', 'size',
                    'investment', 'master')
    list_filter = ('master', 'investment')
    search_fields = ('codename__startswith', 'name__startswith')

    class Meta:
        ordering = ('investment', 'size', 'master')


@admin.register(PoolMember)
class PoolMemberAdmin(admin.ModelAdmin):
    list_display = ('pool', 'user')
    list_filter = ('pool', 'user')

    class Meta:
        ordering = ('pool', 'user')


@admin.register(InvestmentTransaction)
class InvestmentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'transaction_amount',
                    'transaction_from', 'transaction_for_pool', 'transaction_to')
    list_filter = ('transaction_type', 'transaction_for_pool')

    class Meta:
        ordering = ('transaction_for_pool', 'transaction_amount')
