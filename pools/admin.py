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
    list_display = ('type_of_transaction', 'amount', 'user', 'pool')
    list_filter = ('type_of_transaction', 'pool')

    class Meta:
        ordering = ('pool', 'amount')
