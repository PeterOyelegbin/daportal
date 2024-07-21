from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import UserModel
from .forms import UserCreationForm, UserUpdateForm
from managers import send_async_email
import threading


# Create your views here.
@login_required(login_url='login')
def createUser(request):
    if request.method == 'POST':
        formset = UserCreationForm(request.POST)
        try:
            if request.user.role != 'IT':
                messages.error(request, "Unauthorized to perform this action!")
                return redirect('home')
            if formset.is_valid():
                email = formset.cleaned_data['email']
                if UserModel.objects.filter(email=email).exists():
                    messages.error(request, 'User already exists!')
                else:
                    user = formset.save()
                    # Asynchronously handle send mail
                    threading.Thread(target=send_async_email, args=(
                        'DA Portal: User Created',
                        f"""Dear {user.first_name} {user.last_name},\n\nCongratulations! You have been successfully created on the DA Portal of the ALERT GROUP. Your default password is {formset.cleaned_data['password']}. Please log in and change it.\n\nRegards,\nDA Portal\nhttps://dap-alertgroup.com.ng""",
                        settings.EMAIL_HOST_USER,
                        [user.email]
                    )).start()
                    messages.success(request, 'User added successfully')
                    return redirect('users')
            else:
                messages.error(request, formset.errors)
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
    else:
        formset = UserCreationForm()
    return render(request, 'registration/createUser.html', {'formset': formset})


def loginUser(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email.lower(), password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email or password is incorrect!')
        except Exception as e:
            messages.error(request, f"Error logging in: {str(e)}")
    return render(request, 'registration/login.html')


@login_required(login_url='login')
def logoutUser(request):
    try:
        logout(request)
        messages.success(request, 'Logged out successfully')
    except Exception as e:
        messages.error(request, f"Error logging out: {str(e)}")
    return redirect('home')


@login_required(login_url='login')
def listUsers(request):
    try:
        q = request.GET.get('q', '')
        users = UserModel.objects.filter(first_name__icontains=q)
    except Exception as e:
        messages.error(request, f"Error fetching users: {str(e)}")
        users = []
    return render(request, 'registration/listUsers.html', {'staffs': users})


@login_required(login_url='login')
def userDetails(request, pk):
    try:
        user = get_object_or_404(UserModel, id=pk)
    except Exception as e:
        messages.error(request, f"User does not exist: {str(e)}")
        return redirect('users')
    return render(request, 'registration/userDetails.html', {'staff': user})


@login_required(login_url='login')
def updateUser(request, pk):
    try:
        user = get_object_or_404(UserModel, id=pk)
        formset = UserUpdateForm(request.POST or None, instance=user)
        if request.method == 'POST':
            if request.user.role != 'IT':
                messages.error(request, "Unauthorized to perform this action!")
                return redirect('home')
            if formset.is_valid():
                formset.save()
                messages.success(request, 'User data successfully updated')
                return redirect('user_details', pk=pk)
    except Exception as e:
        messages.error(request, f"Error updating user: {str(e)}")
        formset = UserUpdateForm(instance=user)
    return render(request, 'registration/updateUser.html', {'formset': formset})


@login_required(login_url='login')
def deleteUser(request, pk):
    try:
        user = get_object_or_404(UserModel, id=pk)
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'User deleted successfully')
            return redirect('users')
    except Exception as e:
        messages.error(request, f"Error deleting user: {str(e)}")
    return render(request, 'registration/deleteUser.html', {'user': user})
