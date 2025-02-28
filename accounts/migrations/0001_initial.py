# Generated by Django 3.1.5 on 2021-06-06 13:40

import config.validators
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(help_text='Your valid mobile number for OTP verification.', max_length=12, unique=True, validators=[config.validators.validate_username], verbose_name='Contact Number')),
                ('first_name', models.CharField(blank=True, help_text='Your first name. (to be used in future transactions)', max_length=26, validators=[config.validators.validate_name], verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, help_text='Your last name. (to be used in future transactions)', max_length=26, validators=[config.validators.validate_name], verbose_name='Last Name')),
                ('picture', models.ImageField(blank=True, help_text='Your recent picture (must match with picture in photo ID below) in .png or .jpg format. (Max 2 MB)', upload_to='picture/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Profile Picture')),
                ('aadhaar_number', models.CharField(blank=True, help_text='Your 12 digit Aadhaar Number (as written on your aadhaar card).', max_length=12, validators=[config.validators.validate_aadhaar_number], verbose_name='Aadhaar Card Number')),
                ('pan_number', models.CharField(blank=True, help_text='Your 10 digit PAN Number (as written on your PAN card).', max_length=10, validators=[config.validators.validate_pan_number], verbose_name='PAN Card Number')),
                ('identity_proof', models.ImageField(blank=True, help_text='Your photo ID proof (preferably Aadhaar Card) in .png or .jpg format. (Max 2 MB)', upload_to='identity/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Identity Proof Photograph')),
                ('identity_verified', models.BooleanField(default=False)),
                ('identity_reject_reason', models.CharField(blank=True, help_text="The reason to Reject user's Identity Verification (by Internal Team).", max_length=250, verbose_name='ID Proof Rejection Reason')),
                ('contact_secret', models.CharField(blank=True, max_length=16)),
                ('contact_verified', models.BooleanField(default=False)),
                ('is_willing_master', models.BooleanField(default=False)),
                ('balance_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.DecimalValidator, config.validators.validate_amount], verbose_name='Balance Amount')),
                ('investment_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[django.core.validators.DecimalValidator, config.validators.validate_amount], verbose_name='Investment Amount')),
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
            name='BalanceTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=250, unique=True)),
                ('payment_id', models.CharField(blank=True, max_length=250)),
                ('payment_signature', models.CharField(blank=True, max_length=250)),
                ('type_of_transaction', models.CharField(choices=[('C', 'Credit'), ('D', 'Debit')], max_length=1, validators=[config.validators.validate_balance_type_of_transaction])),
                ('amount', models.DecimalField(decimal_places=2, help_text='The amount in INR to be added (Taxes will be added on this amount)', max_digits=9, validators=[config.validators.validate_amount])),
                ('tax', models.DecimalField(decimal_places=2, max_digits=9, validators=[config.validators.validate_amount])),
                ('verified', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccountDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(help_text='Name of Bank', max_length=64, validators=[config.validators.validate_name], verbose_name='Bank Name')),
                ('account_number', models.CharField(help_text='Your Account Number', max_length=64, verbose_name='Account Number')),
                ('ifsc_code', models.CharField(help_text='Your IFSC Code', max_length=64, verbose_name='IFSC Code')),
            ],
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name for Billing', max_length=64, validators=[config.validators.validate_name], verbose_name='Full Name')),
                ('address1', models.CharField(help_text='Line 1 of the Address', max_length=128, verbose_name='Address Line 1')),
                ('address2', models.CharField(help_text='Line 2 of the Address', max_length=128, verbose_name='Address Line 2')),
                ('zip_code', models.CharField(help_text='ZIP / Postal code for the Address', max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(help_text='City for the Address', max_length=128, verbose_name='City')),
                ('state', models.CharField(help_text='State for the Address', max_length=128, verbose_name='State')),
                ('country', models.CharField(choices=[('IN', 'India')], max_length=3, verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='ContactNumberOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(editable=False, max_length=12, validators=[config.validators.validate_username])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_transaction', models.CharField(choices=[('I', 'Invest'), ('D', 'Disinvest')], max_length=1, validators=[config.validators.validate_investment_type_of_transaction])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7, validators=[config.validators.validate_amount])),
                ('verified', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_ticket', models.CharField(choices=[('F', 'Finance Related'), ('A', 'Application Related')], max_length=1, validators=[config.validators.validate_support_ticket_type_of_ticket])),
                ('user_message', models.TextField(blank=True, help_text='Please elaborate the issues you are facing.', max_length=1000, validators=[config.validators.validate_message], verbose_name='Description of Issue')),
                ('manager_message', models.TextField(blank=True, help_text='Please elaborate the resolution of the issue.', max_length=1000, validators=[config.validators.validate_message], verbose_name='Resolution Response')),
                ('closed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='support_ticket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
