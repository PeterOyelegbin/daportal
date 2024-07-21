from django.forms import ModelForm, ChoiceField, Select, TextInput, EmailInput, PasswordInput
from managers import ORGANIZATION, BRANCH, ROLE
from .models import UserModel


class UserCreationForm(ModelForm):
    organization = ChoiceField(choices=ORGANIZATION, widget=Select(attrs={"class":"form-control"}))
    role = ChoiceField(choices=ROLE, widget=Select(attrs={"class":"form-control"}))
    branch = ChoiceField(choices=BRANCH, widget=Select(attrs={"class":"form-control"}))
    
    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "organization", "role", "branch", "email", "password", "is_active"]
        widgets = {
            "first_name": TextInput(attrs={"class":"form-control"}),
            "last_name": TextInput(attrs={"class":"form-control"}),
            "email": EmailInput(attrs={"class":"form-control", "placeholder":"example@alertgroup.com.ng"}),
            "password": PasswordInput(attrs={"class":"form-control"}), 
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(ModelForm):
    organization = ChoiceField(choices=ORGANIZATION, widget=Select(attrs={"class":"form-control"}))
    role = ChoiceField(choices=ROLE, widget=Select(attrs={"class":"form-control"}))
    branch = ChoiceField(choices=BRANCH, widget=Select(attrs={"class":"form-control"}))
    
    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "organization", "role", "branch", "is_active"]
        widgets = {
            "first_name": TextInput(attrs={"class":"form-control"}),
            "last_name": TextInput(attrs={"class":"form-control"}),
        }
