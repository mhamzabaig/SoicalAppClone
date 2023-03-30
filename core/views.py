from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/signin')
def index(request):
    return render(request,'index.html')

def SignIn(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials ')
            return redirect('/signin')
    else:
        return render(request,'signin.html')


def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email alread existed ")
                redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username alread existed ")
                redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                # Create a new Profile
                user_model = User.objects.get(username=username)
                newProfile = Profile.objects.create(user=user_model,id_user=user_model.id)
                newProfile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not Matching ')
            return redirect('signup')
    else: return render(request,'signup.html')

@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/signin')

@login_required(login_url='/signin')
def settings(request):
    return render(request,'settings.html')