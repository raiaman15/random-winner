# Generated by Django 3.1.5 on 2021-02-05 23:53

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
                ('size', models.IntegerField(default=20, help_text='Pool size, i.e. maximum member count for the Pool', validators=[config.validators.validate_pool_size], verbose_name='Pool Size')),
                ('investment', models.DecimalField(decimal_places=2, default=10000, max_digits=7, validators=[config.validators.validate_investment], verbose_name='Pool Investment Amount')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('activated', models.DateTimeField(blank=True, null=True)),
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
        migrations.CreateModel(
            name='PoolInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=12, unique=True, validators=[config.validators.validate_username])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pools.pool')),
            ],
        ),
        migrations.AddField(
            model_name='pool',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_of_pool', through='pools.PoolMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
