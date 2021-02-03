"""
Creates necessary permission groups for users
It uses the DATA/group_permission.csv for its input
"""
import logging
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

# python manage.py guard_seed

# Permissions: delete, change, add, view
# 0 - 0000 - no delete, no change, no add, no view
# 1 - 0001 - no delete, no change, no add, yes view
# 2 - 0010 - no delete, no change, yes add, no view
# 3 - 0011 - no delete, no change, yes add, yes view
# 4 - 0100 - no delete, yes change, no add, no view
# 5 - 0101 - no delete, yes change, no add, yes view
# 6 - 0110 - no delete, yes change, yes add, no view
# 7 - 0111 - no delete, yes change, yes add, yes view
# 8 - 1000 - yes delete, no change, no add, no view
# 9 - 1001 - yes delete, no change, no add, yes view
# 10 - 1010 - yes delete, no change, yes add, no view
# 11 - 1011 - yes delete, no change, yes add, yes view
# 12 - 1100 - yes delete, yes change, no add, no view
# 13 - 1101 - yes delete, yes change, no add, yes view
# 14 - 1110 - yes delete, yes change, yes add, no view
# 15 - 1111 - yes delete, yes change, yes add, yes view

PERMISSIONS = {
    0: ['clear'],
    1: ['view'],
    2: ['add'],
    3: ['view', 'add'],
    4: ['change'],
    5: ['view', 'change'],
    6: ['add', 'change'],
    7: ['view', 'add', 'change'],
    8: ['delete'],
    9: ['view', 'delete'],
    10: ['add', 'delete'],
    11: ['view', 'add', 'delete'],
    12: ['change', 'delete'],
    13: ['view', 'change', 'delete'],
    14: ['add', 'change', 'delete'],
    15: ['view', 'add', 'change', 'delete'],
}


class Command(BaseCommand):
    help = 'Creates necessary permission groups for users'

    def handle(self, *args, **options):
        self.stdout.write('\nSeeding Accounts Module Data...')
        run_group_permission_seed(self)
        self.stdout.write('Accounts Module Data Loaded')


def grant_permission(group_name, model_name, permission_names):

    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f'+ Created new group: {group_name}')

    for permission_name in permission_names:
        name = f'Can {permission_name} {model_name}'
        try:
            model_perm = Permission.objects.get(name=name)
            group.permissions.add(model_perm)
        except Permission.DoesNotExist:
            logging.warning(f'Permission not found with name {name}.')

    return print(f'\u2713 {group_name} can {", ".join(permission_names)} {model_name}')


def run_group_permission_seed(self):
    # Creates Group and Grants Permission
    pd.read_csv('./DATA/group_permission.csv').apply(lambda x: grant_permission(
        group_name=x['group'], model_name=x['model'], permission_names=PERMISSIONS[x['permission']]), axis=1)
