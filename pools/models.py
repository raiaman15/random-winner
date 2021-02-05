from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from config.validators import validate_investment, validate_name, validate_number, validate_investment_type_of_transaction, validate_amount, validate_pool_size


class Pool(models.Model):
    codename = models.CharField(
        'Pool Codename',
        blank=False, unique=True, max_length=250,
        help_text='Codename for the Pool'
    )
    name = models.CharField(
        'Pool Name',
        blank=False, unique=False, max_length=250,
        validators=[validate_name], help_text='Name for the Pool'
    )
    size = models.IntegerField(
        'Pool Size',
        default=20, null=False, blank=False, validators=[validate_pool_size],
        help_text='Pool size, i.e. maximum member count for the Pool'
    )
    investment = models.DecimalField(
        'Pool Investment Amount',
        default=10000, max_digits=7, decimal_places=2, validators=[validate_investment], null=False, blank=False,
    )
    master = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name='master_of_pool', blank=False,
    )
    members = models.ManyToManyField(
        get_user_model(), through="PoolMember", related_name='member_of_pool', blank=True
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        """ Save only if the Master of Pool is verified by Manager
        and if the investment amount if a multiple of a decided amount. 
        Generates codename (Limits 1 pool creation per minute)
        """
        prefix = self.master[:3]
        t = timezone.now()
        yy = t.strftime("%Y")
        mm = t.strftime("%m")
        dd = t.strftime("%d")
        hh = t.strftime("%H")
        mm = t.strftime("%M")
        self.codename = prefix+yy+mm+dd+hh+mm
        if self.master.groups.filter(name='master').exists() and self.investment % 10000 == 0:
            super(Pool, self).save(*args, **kwargs)

    def get_member_count(self):
        """ Gets the count of members who have joined the pool """
        return self.members.count()

    def get_member_remaining(self):
        """ Gets the count of remaining members before the pool gets full """
        return self.size - self.members.count()

    def is_master(self, user):
        """ Checks if the user is master of this pool """
        return self.master == user

    def is_member(self, user):
        """ Checks if the user is member of this pool """
        return user in self.members

    def can_join_pool(self, user):
        """ Checks if pool is available and user is not already in the pool """
        if self.get_member_remaining > 0:
            if not self.is_member(user):
                return True
        return False

    def invite(self, user):
        """ Invites a user in this pool """
        """ Checks if user haven't been invited previously """
        if self.can_join_pool(user):
            if not PoolInvite.objects.filter(pool=self, user=user).exists():
                PoolInvite(pool=self, user=user).save()
                return True
        return False

    def initiate_join(self, user):
        """ Initiates a Transaction to Join the Pool """
        # Refresh User's Balance
        
        # If they have sufficient balance
        InvestmentTransaction(
            type_of_transaction='I',
            amount=self.investment,
            user=user,
            pool=self
        ).save()
        # Refresh User's Balance


    def get_absolute_url(self):
        return reverse('pool_detail', args=[str(self.id)])

    def __str__(self):
        return self.name + ':' + self.master


class PoolMember(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)


class PoolInvite(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    accept = models.BooleanField(default=False)


class InvestmentTransaction(models.Model):
    TRANSACTION_TYPE = (
        ('I', 'Invest'),
        ('D', 'Disinvest')
    )
    type_of_transaction = models.CharField(
        max_length=1, choices=TRANSACTION_TYPE, blank=False,
        validators=[validate_investment_type_of_transaction]
    )
    amount = models.DecimalField(
        null=False, blank=False, max_digits=7, decimal_places=2,
        validators=[validate_amount]
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='outgoing_investment_transactions', blank=False
    )
    pool = models.ForeignKey(
        Pool, on_delete=models.DO_NOTHING, related_name='investment_transactions', blank=False
    )
    verified = models.BinaryField(default=False, editable=True)

    def __str__(self):
        return self.user + ':' + self.type_of_transaction + ':' + self.pool + ':' + str(self.amount)
