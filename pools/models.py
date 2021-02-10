import pyotp
import random
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from config.validators import validate_username, validate_investment, validate_name, validate_number, validate_amount, validate_pool_size
from config.utils import send_sms_pool_invite, send_email_pool_invite, send_sms_platform_invite, send_email_pool_winner, send_sms_pool_winner
from accounts.models import InvestmentTransaction


class Pool(models.Model):
    codename = models.CharField(
        'Pool Codename', blank=False, unique=True, max_length=250,
        help_text='Codename for the Pool'
    )
    name = models.CharField(
        'Pool Name', blank=False, unique=False, max_length=250,
        validators=[validate_name], help_text='Name for the Pool'
    )
    size = models.IntegerField(
        'Pool Size', default=20, null=False, blank=False, validators=[validate_pool_size],
        help_text='Pool size, i.e. maximum member count for the Pool'
    )
    investment = models.DecimalField(
        'Pool Investment Amount', default=10000, max_digits=7, decimal_places=2, validators=[validate_investment], null=False, blank=False
    )
    master = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='master_of_pool', blank=False)
    members = models.ManyToManyField(get_user_model(), through="PoolMember", related_name='member_of_pool', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    activated = models.DateTimeField(blank=True, null=True)

    def save(self):
        self.full_clean()
        super(Pool, self).save()

    def get_member_count(self):
        """ Gets the count of members who have joined the pool """
        return self.members.count()

    def get_member_remaining(self):
        """ Gets the count of remaining members for the pool """
        return self.size - self.members.count()

    def is_master(self, user):
        """ Checks if the user is master of this pool """
        return self.master == user

    def is_member(self, user):
        """ Checks if the user is member of this pool """
        return user in self.members.all()

    def can_join_pool(self, user):
        """ Checks if the User is elidgible to join any pool """
        """ Checks if pool is available and user is not already in the pool """
        if user.groups.filter(name='member').exists():
            if self.get_member_remaining() > 0:
                if not self.is_member(user):
                    if not self.activated:
                        return True

    def invite(self, username):
        """ Invites a user in this pool """
        """ Checks if users can be invited in the Pool """
        if self.get_member_remaining() > 0:
            PoolInvite(pool=self, username=username).save()

    def activate(self, user):
        """ Checks if the pool is filled """
        """ Activates the pool if filled """
        if self.get_member_remaining() == 0:
            self.activated = timezone.now()

    def join(self, user):
        """ Initiates a Transaction to Join the Pool """
        if self.can_join_pool(user):
            user.refresh_balance_investment()
            if user.balance_amount > self.investment:
                it = InvestmentTransaction(type_of_transaction='I', amount=self.investment, user=user, pool=self)
                it.save()
                if self.get_member_remaining() > 0:
                    self.members.add(user)
                    it = InvestmentTransaction.objects.get(id=it.id)
                    it.verified = True
                    it.save()
                    return True
                else:
                    InvestmentTransaction.objects.filter(id=it.id).delete()
            else:
                raise ValueError('Insufficient Balance Amount')
            user.refresh_balance_investment()

    def spin(self):
        if not self.activate:
            raise ValueError('The pool is still not active. Wait for other members to join!')
        else:
            lower_limit = 1
            upper_limit = self.get_member_count()+1
            selected = random.randint(lower_limit, upper_limit)
            user = self.members[selected]
            winner = PoolWinner(pool=self, user=user)
            winner.save()
            self.exit(user)

    def exit(self, user):
        """ Initiates a Transaction to Join the Pool """
        incentive = 0
        if not self.activate:
            raise ValueError('The pool is still not active. Wait for other members to join!')
        else:
            now = timezone.now()
            yd = now.year - self.activated.year
            md = now.month - self.activated.month
            month = int((yd * 12) + md)
            incentive = (0.05*self.investment)*month  # 5% of investment per month
        if self.is_member(user):
            # Refresh User's Balance
            user.refresh_balance_investment()
            # If they have sufficient balance
            if user.balance_amount > self.investment:
                # Initiate Transaction for User & Master
                InvestmentTransaction(
                    type_of_transaction='D', amount=self.investment + incentive,
                    user=user, pool=self).full_clean().create()
                InvestmentTransaction(
                    type_of_transaction='D', amount=self.investment + incentive,
                    user=self.master, pool=self).full_clean().create()
                # Remove the User from the Pool
                self.members.remove(user)
                # Complete Transaction for User & Master
                itu = InvestmentTransaction.objects.filter(
                    type_of_transaction='D', amount=self.investment + incentive, user=user, pool=self)
                itm = InvestmentTransaction.objects.filter(
                    type_of_transaction='D', amount=self.investment + incentive, user=self.master, pool=self)
                itu.verified, itm.verified = True, True
                itu.full_clean().save()
                itm.full_clean().save()
                # SMS & e-Mail Notification of Transaction
                send_email_pool_winner(email=user.email, pool_id=self.id)
                send_sms_pool_winner(number=user.username, pool_id=self.id)
                # Refresh User's Balance
                user.refresh_balance_investment()

    def get_absolute_url(self):
        return reverse('pool_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} : {self.master.username}'


class PoolMember(models.Model):
    pool = models.ForeignKey('pools.Pool', on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, editable=False)


class PoolInvite(models.Model):
    pool = models.ForeignKey('pools.Pool', related_name='invitations', on_delete=models.CASCADE)
    username = models.CharField(
        max_length=12, blank=False, unique=True, validators=[validate_username],
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Sends E-Mail & SMS invite to join the pool if user exist in system
        Create User Account & send invite along with their login credentials
        """
        if not PoolInvite.objects.filter(pool=self, username=username).exists():
            if get_user_model().objects.filter(username=self.username).exists():
                user = get_user_model().objects.get(username=self.username)
                send_sms_pool_invite(user.username, self.pool.id)
                if user.email:
                    send_email_pool_invite(user.email, self.pool.id)
            else:
                password = pyotp.random_base32()
                get_user_model().objects.create_user(username=self.username, password=password)
                send_sms_platform_invite(self.username, self.username, password)
                send_sms_pool_invite(self.username, self.pool.id)
            return super(PoolInvite, self).save(*args, **kwargs)
        else:
            raise ValueError('User is already invited once in this pool!')

    def __str__(self):
        return f'{self.pool} : {self.username}'


class PoolWinner(models.Model):
    pool = models.ForeignKey('pools.Pool', on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self):
        self.full_clean()
        if PoolWinner.objects.filter(pool=self.pool, user=self.user).exists():
            raise ValueError('The user is already out of Pool!')
        else:
            return super(PoolWinner, self).save()
