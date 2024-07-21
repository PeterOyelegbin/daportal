from django.forms import ModelForm, ModelChoiceField, ChoiceField, Select, TextInput, NumberInput, FileInput, CheckboxInput
from .models import UserModel, AccountOpening, LoanApplication
from managers import BRANCH


# Account upload form
class AcctUploadForm(ModelForm):
    branch = ChoiceField(choices=BRANCH, widget=Select(attrs={"class":"form-control"}))
    supervisor = ModelChoiceField(queryset=UserModel.objects.filter(role="HOP", organization="ABL", is_active=True), widget=Select(attrs={"class":"form-control"}))
    
    class Meta:
        model = AccountOpening
        fields = ["full_name", "account_no", "branch", "account_file", "supervisor", "upload_officer"]
        labels = {
            "account_file": "Upload File (rename file to 'customer-name_account-no' before upload)",
            "upload_officer": "",
        }
        widgets = {
            "full_name": TextInput(attrs={"class":"form-control"}),
            "account_no": NumberInput(attrs={"class":"form-control"}),
            "account_file": FileInput(attrs={"class":"form-control"}),
            "upload_officer": TextInput(attrs={"class":"form-control", "id":"upload_officer", "value": "", "type":"hidden"}),
        }

# Account approval form
class AcctApprovalForm(ModelForm):
    class Meta:
        model = AccountOpening
        fields = ["approval_status"]
        widgets = {
            "approval_status": CheckboxInput(),
        }


# Loan upload form
class LoanUploadForm(ModelForm):
    branch = ChoiceField(choices=BRANCH, widget=Select(attrs={"class":"form-control"}))
    approval_officer = ModelChoiceField(queryset=UserModel.objects.filter(role="Credit", organization="ABL", is_active=True), widget=Select(attrs={"class":"form-control"}))
    
    class Meta:
        model = LoanApplication
        fields = ["full_name", "account_no", "branch", "loan_form", "offer_letter", "cam_file", "other_files", "approval_officer", "upload_officer"]
        labels = {
            "loan_form": "Upload Loan form (rename file to 'customer-name_account-no' before upload)",
            "offer_letter": "Upload Offer letter (rename file to 'customer-name_account-no' before upload)",
            "cam_file": "Upload CAM file (rename file to 'customer-name_account-no' before upload)",
            "other_files": "Upload Other files (zip all other files and rename to 'customer-name_account-no' before upload)",
            "upload_officer": "",
        }
        widgets = {
            "full_name": TextInput(attrs={"class":"form-control"}),
            "account_no": NumberInput(attrs={"class":"form-control"}),
            "loan_form": FileInput(attrs={"class":"form-control"}),
            "offer_letter": FileInput(attrs={"class":"form-control"}),
            "cam_file": FileInput(attrs={"class":"form-control"}),
            "other_files": FileInput(attrs={"class":"form-control"}),
            "upload_officer": TextInput(attrs={"class":"form-control", "id":"upload_officer", "value": "", "type":"hidden"}),
        }

# Loan approval form
class LoanApprovalForm(ModelForm):
    class Meta:
        model = LoanApplication
        fields = ["approval_status"]
        widgets = {
            "approval_status": CheckboxInput(),
        }
