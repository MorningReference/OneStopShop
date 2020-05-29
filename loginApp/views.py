from django.shortcuts import render, redirect
from .models import *
from productsApp.models import *
from .forms import *


from django.contrib import messages
import bcrypt

def showLogin(request):
    # If the user is already logged in, they cannot navigate to the login/registration page
    # if 'user_id' in request.session:
    #     return redirect('/home')
    # form = RegisterForm()
    # context = {
    #     'regForm': form
    # }
    return render(request, 'login.html')

def showRegister(request):
    # If the user is already logged in, they cannot navigate to the login/registration page
    # if 'user_id' in request.session:
    #     return redirect('/home')
    return render(request, 'register.html')

def register(request):
    # Redirect users who navigate to this page without sending a form
    if request.method == "GET":
        return redirect('/home')
    errors = User.objects.registration_validation(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/user/register')

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        birth_date = request.POST['birth_date'],
        password = pw_hash
    )
    request.session['user_id'] = new_user.id
    return redirect('/home')

def login(request):
    # Redirect users who navigate to this page without sending a form
    if request.method == "GET":
        return redirect('/home')

    user = User.objects.filter(email = request.POST['login_email'])
    if user:
        if bcrypt.checkpw(request.POST['login_pw'].encode(), user[0].password.encode()):
            request.session['user_id'] = user[0].id
            return redirect('/home')

    messages.error(request, "Invalid email/password", extra_tags="login_email")
    return redirect('/user')


def editUser(request, userId=1):
    # Returns to main page if the user is not logged in
    if 'user_id' not in request.session:
        return redirect('/home')
    
    # If the user is not the same user who we're going to be editing, returns them to the main page
    if request.session['user_id'] != userId:
        return redirect('/home')

    user = User.objects.filter(id = request.session['user_id'])[0]
    context = {
        'user': user,
        'shipping_addresses': ShippingInfo.objects.filter(user = user),
        'stored_payment': PaymentInfo.objects.filter(user = user),
    }
    return render(request, 'editUser.html', context) # Renders the page and passes in the user object

def updateUser(request, userId, updateType):
    # Returns to main page if the user is not logged in
    if 'user_id' not in request.session:
        return redirect('/home')
    # If a user navigates to this page, it returns them to the previous edit page
    if request.method == "GET":
        return redirect(f'/user/myaccount/{userId}')
    # If the user does not match the user logged in, it returns them to the main page
    if request.session['user_id'] != userId:
            return redirect('/home')

    if(updateType == 'info'):
        errors = User.objects.update_info_validation(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect(f'/user/myaccount/{userId}')
        
        user = User.objects.filter(id = userId)[0]
        user.first_name = request.POST['updated_first_name']
        user.last_name = request.POST['updated_last_name']
        user.email = request.POST['updated_email']
        user.save()
        return redirect(f'/user/myaccount/{userId}')

    elif(updateType == 'password'):
        errors = User.objects.update_password_validation(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect(f'/user/myaccount/{userId}')

        pw_hash = bcrypt.hashpw(request.POST['updated_password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.filter(id = userId)[0]
        user.password = pw_hash
        user.save()
        return redirect(f'/user/myaccount/{userId}')

def logout(request):
    request.session.flush()
    return redirect('/')
