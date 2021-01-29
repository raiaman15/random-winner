# Generated by Django 3.1.5 on 2021-01-29 21:38

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
                ('name', models.CharField(editable=False, help_text='Unique name for the Pool', max_length=250, unique=True)),
                ('size', models.IntegerField(default=20, help_text='Pool size, i.e. maximum member count for the Pool')),
                ('investment', models.DecimalField(decimal_places=2, default=10000, editable=False, max_digits=7, validators=[config.validators.validate_investment])),
                ('master', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='master_of_pools', to=settings.AUTH_USER_MODEL)),
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
            field=models.ManyToManyField(blank=True, related_name='member_of_pools', through='pools.PoolMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='InvestmentTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('I', 'Invest'), ('D', 'Disinvest')], max_length=1)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('transaction_for_pool', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='investment_transactions', to='pools.pool')),
                ('transaction_from', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='outgoing_investment_transactions', to=settings.AUTH_USER_MODEL)),
                ('transaction_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='incoming_investment_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
