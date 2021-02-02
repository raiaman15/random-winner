# Generated by Django 3.1.5 on 2021-02-02 19:12

import config.validators
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, help_text='Your first name. (to be used in future transactions)', max_length=26, validators=[config.validators.validate_name])),
                ('last_name', models.CharField(blank=True, help_text='Your last name. (to be used in future transactions)', max_length=26, validators=[config.validators.validate_name])),
                ('picture', models.ImageField(blank=True, help_text='Your recent picture (must match with picture in photo ID below) in .png or .jpg format. (Max 2 MB)', upload_to='picture/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('aadhaar_number', models.CharField(blank=True, help_text='Your 12 digit Aadhaar Number (as written on your aadhaar card).', max_length=12, validators=[config.validators.validate_aadhaar_number])),
                ('pan_number', models.CharField(blank=True, help_text='Your 10 digit PAN Number (as written on your PAN card).', max_length=10, validators=[config.validators.validate_pan_number])),
                ('identity_proof', models.ImageField(blank=True, help_text='Your photo ID proof (preferably Aadhaar Card) in .png or .jpg format. (Max 2 MB)', upload_to='identity/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('identity_verified', models.BooleanField(default=False)),
                ('identity_reject_reason', models.CharField(blank=True, help_text="The reason to Reject user's Identity Verification (by Internal Team).", max_length=250)),
                ('contact_number', models.CharField(blank=True, help_text='Your valid mobile number for OTP verification.', max_length=12, validators=[config.validators.validate_conatct_number])),
                ('contact_secret', models.CharField(blank=True, max_length=16)),
                ('contact_verified', models.BooleanField(default=False)),
                ('is_willing_master', models.BooleanField(default=False)),
                ('is_verified_master', models.BooleanField(default=False)),
                ('balance_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[django.core.validators.DecimalValidator, config.validators.validate_amount])),
                ('investment_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[django.core.validators.DecimalValidator, config.validators.validate_amount])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContactNumberOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(editable=False, max_length=17, unique=True, validators=[config.validators.validate_conatct_number])),
                ('otp', models.CharField(editable=False, max_length=6, validators=[config.validators.validate_otp])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BalanceTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('D', 'Debit'), ('C', 'Credit')], max_length=1, validators=[config.validators.validate_balance_transaction_type])),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=7, validators=[config.validators.validate_amount])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transaction_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='balance_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
