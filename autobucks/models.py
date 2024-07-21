from django.db import models
from django.core.validators import MinLengthValidator
from uuid import uuid4
from accounts.models import UserModel
from managers import acct_file_size, loan_file_size, zip_file_size


# Create your models here.
class AccountOpening(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    full_name = models.CharField(max_length=255)
    account_no = models.CharField(max_length=17, validators=[MinLengthValidator(17, 'minimum of 17 characters required')])
    branch = models.CharField(max_length=100)
    account_file = models.FileField(upload_to='account_files', validators=[acct_file_size])
    supervisor = models.ForeignKey(UserModel, related_name="ABL_HOP", on_delete=models.CASCADE)
    upload_officer = models.ForeignKey(UserModel, related_name="ABL_CSO", on_delete=models.PROTECT)
    approval_status = models.BooleanField(verbose_name="Approved", default="False")
    date_uploaded = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'abl_accountopening'
        ordering = ['-date_uploaded']


class LoanApplication(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    full_name = models.CharField(max_length=255)
    account_no = models.CharField(max_length=17, validators=[MinLengthValidator(17, 'minimum of 17 characters required')])
    branch = models.CharField(max_length=100)
    loan_form = models.FileField(upload_to='loan_forms', validators=[loan_file_size])
    offer_letter = models.FileField(upload_to='offer_letters', validators=[loan_file_size])
    cam_file = models.FileField(upload_to='cam_files', validators=[zip_file_size ])
    other_files = models.FileField(upload_to='other_files', validators=[zip_file_size])
    approval_officer = models.ForeignKey(UserModel, related_name="ABL_Credit_Officer", on_delete=models.CASCADE)
    upload_officer = models.ForeignKey(UserModel, related_name="ABL_Loan_Officer", on_delete=models.PROTECT)
    approval_status = models.BooleanField(verbose_name="Approved", default="False")
    date_uploaded = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'abl_loanapplication'
        ordering = ['-date_uploaded']
