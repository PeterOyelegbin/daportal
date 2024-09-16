from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
# from django.core.mail import send_mail
from django.core.paginator import Paginator
from datetime import datetime
# from accounts.models import UserModel
from .models import AccountOpening, LoanApplication
from .forms import AcctUploadForm, AcctApprovalForm, LoanUploadForm, LoanApprovalForm
from managers import send_async_email
import threading


# Create your views here.
@login_required(redirect_field_name="login")
def AccountList(request):
    q = request.GET.get('q', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    # Initial queryset
    doc_list = AccountOpening.objects.all()
    # Filter by search query
    if q:
        doc_list = doc_list.filter(Q(full_name__icontains=q) | Q(account_no__icontains=q))
    # Filter by month and year
    if month and year:
        try:
            start_date = datetime(int(year), int(month), 1)
            if int(month) == 12:
                end_date = datetime(int(year) + 1, 1, 1)
            else:
                end_date = datetime(int(year), int(month) + 1, 1)
            doc_list = doc_list.filter(date_uploaded__gte=start_date, date_uploaded__lt=end_date)
        except ValueError as e:
            messages.error(request, f"The error '{e}' occurred while processing your request. Please try again later.")
 
    paginator = Paginator(doc_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_year = datetime.now().year
    years = range(2020, current_year + 1)

    context = {
        'page_obj': page_obj,
        'years': years,
        'q': q,
        'month': month,
        'year': year,
    }
    return render(request, 'alertmfb/account_list.html', context)


@login_required(redirect_field_name="login")
def AccountUpload(request):
    formset = AcctUploadForm()
    if request.method == 'POST':
        formset = AcctUploadForm(request.POST, request.FILES or None)
        if formset.is_valid():
            if request.user.role != 'Upload Officer':
                messages.error(request, 'Unauthorized to perform this action!')
                return redirect('home')
            supervisor = formset.cleaned_data['supervisor']
            try:
                # Asyncronously handle send mail
                threading.Thread(target=send_async_email, args=(
                    'DA Portal: Account File Uploaded',
                    f"""Dear {supervisor},\n\nI have submitted some documents for approval on the DA Portal.
                    Kindly attend to the document as it awaits your approval by searching with '{formset.cleaned_data['full_name']}'\n\nBest regards,
                    \n{request.user.first_name} {request.user.last_name}\n{request.user.email}\nhttps://dap-alertgroup.com.ng""",
                    request.user.email,
                    [supervisor.email]
                )).start()
                formset.save()
                messages.success(request, 'Account document uploaded successfully and awaiting approval')
                return redirect('home')
            except Exception as e:
                messages.error(request, f"The error '{e}' occurred while processing your request. Please try again later.")
                return render(request, 'alertmfb/account_upload.html', {'formset': formset})
        else:
            messages.error(request, formset.errors)
    return render(request, 'alertmfb/account_upload.html', {'formset': formset})


@login_required(redirect_field_name="login")
def AccountDetails(request, pk):
    try:
        doc = get_object_or_404(AccountOpening, id=pk)
        return render(request, 'alertmfb/account_details.html', {'doc': doc})
    except AccountOpening.DoesNotExist:
        messages.error(request, "Account document not found.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"The error '{e}' occurred while retrieving account document details.")
        return redirect('home')


@login_required(redirect_field_name="login") 
def AccountApproval(request, pk):
    page = "account_opening"
    object = get_object_or_404(AccountOpening, id=pk)
    formset = AcctApprovalForm(instance=object)
    if request.method == 'POST':
        formset = AcctApprovalForm(request.POST, request.FILES or None, instance=object)
        if formset.is_valid():
            if request.user.role != 'HOP':
                messages.error(request, 'Unauthorized to perform this action!')
                return redirect('home')
            approval_status = formset.cleaned_data['approval_status']
            if not approval_status:
                messages.error(request, "Account document yet to be approved!")
                return redirect('/amfb/account/approve/'+pk)
            try:
                # Asyncronously handle send mail
                threading.Thread(target=send_async_email, args=(
                    'DA Portal: Account File Approved',
                    f"""Dear {object.upload_officer.first_name},\n\nThe submitted document for '{object}' has been approved upon review.
                    \n\nBest regards,\n{request.user.first_name} {request.user.last_name}\n{request.user.email}\nhttps://dap-alertgroup.com.ng""",
                    request.user.email,
                    [object.upload_officer.email]
                )).start()
                formset.save()
                messages.success(request, 'Account document successfully approved')
                return redirect('home')
            except Exception as e:
                messages.error(request, f"The error '{e}' occurred while processing the account document for approval")
                return redirect('/amfb/account/approve/'+pk)
        else:
            messages.error(request, formset.errors)
    return render(request, 'doc_approve.html', {'page': page, 'formset': formset})


@login_required(redirect_field_name="login")
def AccountRejection(request, pk):
    if request.user.role != 'HOP':
        messages.error(request, 'Unauthorized to perform this action!')
        return redirect('home')
    try:
        object = get_object_or_404(AccountOpening, id=pk)
        # Asyncronously handle send mail
        threading.Thread(target=send_async_email, args=(
            'DA Portal: Account File Rejected',
            f"""Dear {object.upload_officer.first_name},\n\nThe submitted document for '{object}' has been rejected upon review.
            Kindly contact your supervisor/review officer for necessary details that needs to be corrected before reuploading.\n\nBest regards,
            \n{request.user.first_name} {request.user.last_name}\n{request.user.email}\nhttps://dap-alertgroup.com.ng""",
            request.user.email,
            [object.upload_officer.email]
        )).start()
        # Delete associated files and db record
        object.account_file.delete()
        object.delete()
        messages.success(request, 'Account document rejected!')
        return redirect('home')
    except Exception as e:
        messages.error(request, f"The error '{e}' occurred while processing the account document for rejection. Please contact support.")
        return redirect('/amfb/account/details/'+pk)


@login_required(redirect_field_name="login")
def AccountDelete(request, pk):
    if request.user.role != 'IT':
        messages.error(request, 'Unauthorized to perform this action!')
        return redirect('home')
    try:
        object = get_object_or_404(AccountOpening, id=pk)
        # Delete associated files and db record
        object.account_file.delete()
        object.delete()
        messages.success(request, 'Account document delete successfully!')
    except AccountOpening.DoesNotExist:
        messages.error(request, 'Account document not found')
    except Exception as e:
        messages.error(request, f"The error '{e}' occurred while deleting the account document")
        return redirect('home')


# Loan view functions
@login_required(redirect_field_name="login")
def LoanList(request):
    q = request.GET.get('q', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    # Initial queryset
    doc_list = LoanApplication.objects.all()
    # Filter by search query
    if q:
        doc_list = doc_list.filter(Q(full_name__icontains=q) | Q(account_no__icontains=q))
    # Filter by month and year
    if month and year:
        try:
            start_date = datetime(int(year), int(month), 1)
            if int(month) == 12:
                end_date = datetime(int(year) + 1, 1, 1)
            else:
                end_date = datetime(int(year), int(month) + 1, 1)
            doc_list = doc_list.filter(date_uploaded__gte=start_date, date_uploaded__lt=end_date)
        except ValueError as e:
            messages.error(request, f"The error '{e}' occurred while processing your request. Please try again later.")

    paginator = Paginator(doc_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_year = datetime.now().year
    years = range(2020, current_year + 1)

    context = {
        'page_obj': page_obj,
        'years': years,
        'q': q,
        'month': month,
        'year': year,
    }
    return render(request, 'alertmfb/loan_list.html', context)


@login_required(redirect_field_name="login")
def LoanUpload(request):
    formset = LoanUploadForm()
    if request.method == 'POST':
        formset = LoanUploadForm(request.POST, request.FILES or None)
        if formset.is_valid():
            if request.user.role != 'Upload Officer':
                messages.error(request, 'Unauthorized to perform this action!')
                return redirect('amfbLoanList')
            approval_officer = formset.cleaned_data['approval_officer']
            try:
                # Asyncronously handle send mail
                threading.Thread(target=send_async_email, args=(
                    'DA Portal: Loan Documents Uploaded',
                    f"""Dear {approval_officer},\n\nI have submitted some documents for approval on the DA Portal.
                    Kindly attend to the document as it awaits your approval by searching with '{formset.cleaned_data['full_name']}'\n\nBest regards,
                    \n{request.user.first_name} {request.user.last_name}\n{request.user.email}\nhttps://dap-alertgroup.com.ng""",
                    request.user.email,
                    [approval_officer.email, "creditrisk@alertgroup.com.ng"]
                )).start()
                formset.save()
                messages.success(request, 'Loan document uploaded successfully and awaiting approval')
                return redirect('amfbLoanList')
            except Exception as e:
                messages.error(request, f"The error '{e}' occurred while processing your request. Please try again later.")
                return render(request, 'alertmfb/loan_upload.html', {'formset': formset})
        else:
            messages.error(request, formset.errors)
    return render(request, 'alertmfb/loan_upload.html', {'formset': formset})


@login_required(redirect_field_name="login")
def LoanDetails(request, pk):
    try:
        doc = get_object_or_404(LoanApplication, id=pk)
        return render(request, 'alertmfb/loan_details.html', {'doc': doc})
    except LoanApplication.DoesNotExist:
        messages.error(request, "Loan documents not found.")
        return redirect('amfbLoanList')
    except Exception as e:
        messages.error(request, f"The error '{e}' occurred while retrieving loan document details.")
        return redirect('amfbLoanList')


@login_required(redirect_field_name="login")
def LoanApproval(request, pk):
    object = get_object_or_404(LoanApplication, id=pk)
    formset = LoanApprovalForm(instance=object)
    if request.method == 'POST':
        formset = LoanApprovalForm(request.POST, request.FILES or None, instance=object)
        if formset.is_valid():
            if request.user.role != 'Credit':
                messages.error(request, 'Unauthorized to perform this action!')
                return redirect('amfbLoanList')
            approval_status = formset.cleaned_data['approval_status']
            if not approval_status:
                messages.error(request, "Loan document yet to be approved!")
                return redirect('/amfb/loan/approve/'+pk)
            try:
                # Asyncronously handle send mail
                threading.Thread(target=send_async_email, args=(
                    'DA Portal: Loan Approved',
                    f"""Dear {object.upload_officer.first_name},\n\nThe submitted document for '{object}' has been approved upon review.
                    \n\nBest regards,\n{request.user.first_name} {request.user.last_name}\n{request.user.email}\nhttps://dap-alertgroup.com.ng""",
                    request.user.email,
                    [object.upload_officer.email, "creditrisk@alertgroup.com.ng"]
                )).start()
                formset.save()
                messages.success(request, 'Loan document successfully approved')
                return redirect('amfbLoanList')
            except Exception as e:
                messages.error(request, f"The error '{e}' occurred while processing the loan document for approval")
                return redirect('/amfb/loan/approve/'+pk)
        else:
            messages.error(request, formset.errors)
    return render(request, 'doc_approve.html', {'formset': formset})


@login_required(redirect_field_name="login")
def LoanRejection(request, pk):
    if request.user.role != 'Credit':
        messages.error(request, 'Unauthorized to perform this action!')
        return redirect('amfbLoanList')
    try:
        loan_application = get_object_or_404(LoanApplication, id=pk)
        # Asyncronously handle send mail
        threading.Thread(target=send_async_email, args=(
            'DA Portal: Loan Rejected',
            f"""Dear {loan_application.upload_officer.first_name},\n\nThe submitted document for '{loan_application}' has been rejected upon review.
            Kindly contact your Credit Officer for necessary details that needs to be corrected before reuploading.\n\nBest regards,
            \n{request.user.first_name} {request.user.last_name}\n{request.user.email}\nhttps://dap-alertgroup.com.ng""",
            request.user.email,
            [loan_application.upload_officer.email, "creditrisk@alertgroup.com.ng"]
        )).start()
        # Delete associated files and db record
        loan_application.loan_form.delete()
        loan_application.offer_letter.delete()
        loan_application.cam_file.delete()
        loan_application.other_files.delete()
        loan_application.delete()
        messages.success(request, 'Loan documents rejected!')
        return redirect('amfbLoanList')
    except Exception as e:
        messages.error(request, f"The error '{e}' occurred while processing the loan document for rejection. Please contact support.")
        return redirect('/amfb/loan/details/'+pk)


@login_required(redirect_field_name="login")
def LoanDelete(request, pk):
    if request.user.role != 'IT':
        messages.error(request, 'Unauthorized to perform this action!')
        return redirect('amfbLoanList')
    try:
        loan_application = get_object_or_404(LoanApplication, id=pk)
        # Delete associated files and db record
        loan_application.loan_form.delete()
        loan_application.offer_letter.delete()
        loan_application.cam_file.delete()
        loan_application.other_files.delete()
        loan_application.delete()
        messages.success(request, 'Loan document delete successfully!')
    except LoanApplication.DoesNotExist:
        messages.error(request, 'Loan document not found')
    except Exception as e:
        messages.error(request, f"The error '{e}' occurred while deleting the loan document")
    return redirect('amfbLoanList')
