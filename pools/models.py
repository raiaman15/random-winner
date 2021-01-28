from django.db import models
from accounts.models import CustomUser
from .validators import validate_investment


class Pool(models.Model):
    size = models.IntegerField(default=20, null=False, blank=False)
    investment = models.DecimalField(
        default=10000, validators=[validate_investment], null=False, blank=False
    )
    master = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='master', blank=False
    )
    members = models.ManyToManyField(
        CustomUser, on_delete=models.PROTECT, related_name='member', blank=True
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
        if self.get_member_remaining > 0:
            if self.master != user:
                self.members.add(user)


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
        CustomUser, on_delete=models.DO_NOTHING, related_name='outgoing_transactions', blank=False
    )
    transaction_for_pool = models.ForeignKey(
        Pool, on_delete=models.DO_NOTHING, related_name='transactions', blank=False
    )
    transaction_to = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='incoming_transactions', blank=False
    )
