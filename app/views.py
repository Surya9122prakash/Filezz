from django.shortcuts import render,redirect
from .models import UploadedFile,ContactMessage
from django.core.files.storage import FileSystemStorage 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError  
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['file'] 
            if uploaded_file:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                uploaded_file_instance = UploadedFile(user=request.user, file=filename)
                uploaded_file_instance.save()
                return redirect('myfiles')
        except MultiValueDictKeyError:
            messages.error(request, "No file selected.")
            return redirect('home')

    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        pass1 = request.POST.get('password')
        myuser = authenticate(request, username=username, password=pass1)
        if myuser is not None:
            login(request, myuser)
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("login")

    return render(request, "login.html")

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('cpassword')

        if pass1 != pass2:
            messages.warning(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username is already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email is already registered")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.save()
        messages.info(request, 'User created successfully')
        return redirect('login')

    return render(request,'register.html')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('login')

@login_required
def myfiles(request):
    user_files = UploadedFile.objects.filter(user=request.user)
    return render(request,"myfiles.html",{'user_files': user_files})

@login_required
def about(request):
    return render(request,"about.html")

@login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_message = ContactMessage(name=name, email=email, message=message)
        contact_message.save()
        return redirect('contact')
    return render(request, 'contact.html')

@login_required
def delete_file(request, file_id):
    file_to_delete = UploadedFile.objects.get(pk=file_id)
    if file_to_delete.user == request.user:
        file_to_delete.file.delete()  
        file_to_delete.delete()
    return HttpResponseRedirect(reverse('myfiles'))
