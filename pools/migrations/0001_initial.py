# Generated by Django 3.1.5 on 2021-02-04 23:57

import config.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(help_text='Codename for the Pool', max_length=250, unique=True, verbose_name='Pool Codename')),
                ('name', models.CharField(help_text='Name for the Pool', max_length=250, validators=[config.validators.validate_name], verbose_name='Pool Name')),
                ('size', models.IntegerField(default=20, help_text='Pool size, i.e. maximum member count for the Pool', validators=[config.validators.validate_number], verbose_name='Pool Size')),
                ('investment', models.DecimalField(decimal_places=2, default=10000, max_digits=7, validators=[config.validators.validate_investment], verbose_name='Pool Investment Amount')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='master_of_pool', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PoolMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pools.pool')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pool',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_of_pool', through='pools.PoolMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='InvestmentTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('I', 'Invest'), ('D', 'Disinvest')], max_length=1, validators=[config.validators.validate_investment_transaction_type])),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=7, validators=[config.validators.validate_amount])),
                ('transaction_for_pool', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='investment_transactions', to='pools.pool')),
                ('transaction_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='outgoing_investment_transactions', to=settings.AUTH_USER_MODEL)),
                ('transaction_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='incoming_investment_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
