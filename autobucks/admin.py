from django.contrib import admin
from .models import AccountOpening, LoanApplication


# Register your models here.
@admin.register(AccountOpening)
class AccountOpeningAdmin(admin.ModelAdmin):
    list_display = ("full_name", "account_no", "approval_status", "date_uploaded")
    list_filter = ("date_uploaded",)

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "account_no", "approval_status", "date_uploaded")
    list_filter = ("date_uploaded",)
