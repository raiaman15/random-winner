from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_investment


class Pool(models.Model):
    name = models.CharField(
        null=False, blank=False, unique=True, editable=False, max_length=250, help_text='Unique name for the Pool')
    size = models.IntegerField(
        default=20, null=False, blank=False, help_text='Pool size, i.e. maximum member count for the Pool')
    investment = models.DecimalField(
        default=10000, max_digits=7, decimal_places=2, validators=[validate_investment], null=False, blank=False, editable=False,
    )
    master = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name='master', blank=False, editable=False,
    )
    members = models.ManyToManyField(
        get_user_model(), through="PoolMember", related_name='member', blank=True
    )

    def save(self, *args, **kwargs):
        """ Save only if the Master of Pool is verified by Manager
        and if the investment amount if a multiple of a decided amount. """
        if self.master.is_verified_master and self.investment % 10000 == 0:
            super(Pool, self).save(*args, **kwargs)

    def get_member_count(self):
        """ Gets the count of members who have joined the pool """
        return len(self.members)

    def get_member_remaining(self):
        """ Gets the count of remaining members before the pool gets full """
        return self.size - len(self.members)

    def verify_master(self, user):
        """ Checks if the user is master of this pool """
        return self.master == user

    def verify_member(self, user):
        """ Checks if the user is member of this pool """
        return user in self.members

    def join_pool(self, user):
        """ Checks if pool is available and user is not already in the pool """
        if self.get_member_remaining > 0:
            if not self.verify_member(user):
                self.members.add(user)

    def __str__(self):
        return self.name + ':' + self.master.email


class PoolMember(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)


class InvestmentTransaction(models.Model):
    TRANSACTION_TYPE = (
        ('I', 'Invest'),
        ('D', 'Disinvest')
    )
    transaction_type = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, blank=False
    )
    transaction_amount = models.DecimalField(
        null=False, blank=False, max_digits=7, decimal_places=2
    )
    transaction_from = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='outgoing_investment_transactions', blank=False
    )
    transaction_for_pool = models.ForeignKey(
        Pool, on_delete=models.DO_NOTHING, related_name='investment_transactions', blank=False
    )
    transaction_to = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='incoming_investment_transactions', blank=False
    )

    def __str__(self):
        return self.transaction_from.email + ':' + self.transaction_type + ':' + self.transaction_for_pool + ':' + self.transaction_amount + ':' + self.transaction_to
