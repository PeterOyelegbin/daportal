# Generated by Django 3.2 on 2024-07-20 13:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('account_no', models.CharField(max_length=17, validators=[django.core.validators.MinLengthValidator(17, 'minimum of 17 characters required')])),
                ('branch', models.CharField(max_length=100)),
                ('loan_form', models.FileField(upload_to='loan_forms', validators=[managers.loan_file_size])),
                ('offer_letter', models.FileField(upload_to='offer_letters', validators=[managers.loan_file_size])),
                ('cam_file', models.FileField(upload_to='cam_files', validators=[managers.zip_file_size])),
                ('other_files', models.FileField(upload_to='other_files', validators=[managers.zip_file_size])),
                ('approval_status', models.BooleanField(default='False', verbose_name='Approved')),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('approval_officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AMFB_Credit_Officer', to=settings.AUTH_USER_MODEL)),
                ('upload_officer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='AMFB_Loan_Officer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'amfb_loanapplication',
                'ordering': ['-date_uploaded'],
            },
        ),
        migrations.CreateModel(
            name='AccountOpening',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('account_no', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10, 'minimum of 10 characters required')])),
                ('branch', models.CharField(max_length=100)),
                ('account_file', models.FileField(upload_to='account_files', validators=[managers.acct_file_size])),
                ('approval_status', models.BooleanField(default='False', verbose_name='Approved')),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AMFB_HOP', to=settings.AUTH_USER_MODEL)),
                ('upload_officer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='AMFB_CSO', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'amfb_accountopening',
                'ordering': ['-date_uploaded'],
            },
        ),
    ]
