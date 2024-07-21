"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from accounts.views import loginUser, listUsers, createUser, userDetails, updateUser, deleteUser, logoutUser
from alertmfb import views as amfb
from autobucks import views as abl
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),

    # User authentication routes
    path('accounts/login/', loginUser, name='login'),
    path('accounts/logout', logoutUser, name='logout'),
    path('accounts/users', listUsers, name='users'),
    path('accounts/create', createUser, name='createUser'),
    path('accounts/users/<pk>', userDetails, name='userDetails'),
    path('accounts/update/<pk>', updateUser, name='updateUser'),
    path('accounts/delete/<pk>', deleteUser, name='deleteUser'),
    
    # Password reset routes
    path('accounts/reset-password', PasswordResetView.as_view(), name="password_reset"),
    path('accounts/reset-password/done', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('accounts/reset-password/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('accounts/reset-password/complete', PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # AMFB account files upload and review routes
    path('', amfb.AccountList, name='home'),
    path('amfb/account/upload', amfb.AccountUpload, name='amfbAcctUpload'),
    path('amfb/account/details/<pk>', amfb.AccountDetails, name='amfbAcctDetails'),
    path('amfb/account/approve/<pk>', amfb.AccountApproval, name='amfbApproveAcct'),
    path('amfb/account/reject/<pk>', amfb.AccountRejection, name='amfbRejectAcct'),
    path('amfb/account/delete/<pk>', amfb.AccountDelete, name='amfbDeleteAcct'),

    # AMFB loan files upload and review routes
    path('amfb/loan/list', amfb.LoanList, name='amfbLoanList'),
    path('amfb/loan/upload', amfb.LoanUpload, name='amfbLoanUpload'),
    path('amfb/loan/details/<pk>', amfb.LoanDetails, name='amfbLoanDetails'),
    path('amfb/loan/approve/<pk>', amfb.LoanApproval, name='amfbApproveLoan'),
    path('amfb/loan/reject/<pk>', amfb.LoanRejection, name='amfbRejectLoan'),
    path('amfb/loan/delete/<pk>', amfb.LoanDelete, name='amfbDeleteLoan'),

    # ABL account files upload and review routes
    path('abl/account/list', abl.AccountList, name='ablAcctList'),
    path('abl/account/upload', abl.AccountUpload, name='ablAcctUpload'),
    path('abl/account/details/<pk>', abl.AccountDetails, name='ablAcctDetails'),
    path('abl/account/approve/<pk>', abl.AccountApproval, name='ablApproveAcct'),
    path('abl/account/reject/<pk>', abl.AccountRejection, name='ablRejectAcct'),
    path('abl/account/delete/<pk>', abl.AccountDelete, name='ablDeleteAcct'),

    # ABL loan files upload and review routes
    path('abl/loan/list', abl.LoanList, name='ablLoanList'),
    path('abl/loan/upload', abl.LoanUpload, name='ablLoanUpload'),
    path('abl/loan/details/<pk>', abl.LoanDetails, name='ablLoanDetails'),
    path('abl/loan/approve/<pk>', abl.LoanApproval, name='ablApproveLoan'),
    path('abl/loan/reject/<pk>', abl.LoanRejection, name='ablRejectLoan'),
    path('abl/loan/delete/<pk>', abl.LoanDelete, name='ablDeleteLoan'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
