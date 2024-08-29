from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
# import openpyxl
from .models import *
from cars.models import *
from .forms import *
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files import File
from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
# from django.core.paginator import Paginator
from django.contrib import messages

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             profile_image = form.cleaned_data.get('profile_image')
#             author = Creator.objects.create(user=user, image=profile_image)
#             auth_login(request, user)
#             return redirect('accounts:authors')
#     else:
#         form = SignUpForm()
#         return render(request, 'registration/signup.html', {'form': form})


def signup(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html', {})

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username:
            messages.error(request, 'username is required')
            return render(request, 'registration/signup.html', {})
        
        # Récupération des données du formulaire
        image = request.FILES.get('image')  # Notez l'utilisation de request.FILES
        job = request.POST['job']
        gender = request.POST['gender']
        email = request.POST['email']
        mobile = request.POST['mobile']


        if not image:
            messages.error(request, 'image is required')
            return render(request, 'registration/signup.html', {})

        # Création de l'objet Car
        User.objects.create(
            username=username, 
            password=password, 
            email=email,
        )
        user = User.objects.get(username=username)
        Creator.objects.create(
            user=user,
            email=email, 
            job=job, 
            gender=gender,
            image=image, 
            mobile=mobile, 
        )
        messages.success(request, 'User saved successfully')

        return redirect('home')




from django.contrib import auth

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                        user.username+' you are now logged in')
                    return redirect('home')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'registration/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'registration/login.html')

    messages.error(
        request, 'Please fill all fields')
    return render(request, 'registration/login.html')
    
    
def logout(request):
    auth_logout(request)
    return render(request, 'registration/login.html',{})


from django.db.models import Q 
def profile(request,user):
    user = User.objects.get(username=user)
    print('User',user)
    if user.is_staff:
        return redirect('cars:home')
    else:
        Creator = get_object_or_404(Creator, user=user)
        print('Creator',Creator)
        activities = Activity.objects.filter(user=Creator.id)
        skills = Language.objects.filter(dev=Creator.id)
        
        # context = {'user':user,'Creator': Creator,'skill':skills[0],
        #             'skills':skills, "job":job , "activities":activities}
        context = {'user':user,'Creator': Creator,'skills':skills,
            "activities":activities}
        return render(request,'accounts/profile.html',context)
        


def profile_edit(request):
    profile = Creator.objects.get(user=request.user)

    if request.method=='POST':
        userform = UserForm(request.POST,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile )
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            return redirect(reverse('accounts:profile'))

    else :
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(request,'accounts/profile_edit.html',{'userform':userform , 'profileform':profileform})



    