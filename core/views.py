from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

@login_required(login_url='/signin')
def index(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    
    return render(request,'index.html',{'user_profile':user_profile,'posts':posts})

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
def upload_post(request):
    if request.method == 'POST':
        user = request.user.username
        img = request.FILES.get('post_image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user,image=img,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return HttpResponse(" Uploading A Post ")

@login_required(login_url='/signin')
def settings(request):
    user_profile= Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') != None:
            print("yes")
            img = request.FILES.get('image')
            bio = request.POST['bio']
            loc = request.POST['location']

            user_profile.profileimg = img
            user_profile.boi = bio
            user_profile.location = loc
            user_profile.save()
            
        elif request.FILES.get('image') == None:
            print("No")
            img = user_profile.profileimg
            bio = request.POST['bio']
            loc = request.POST['location']

            user_profile.profileimg = img
            user_profile.boi = bio
            user_profile.location = loc
            user_profile.save()
        return redirect('settings')    
    
    return render(request,'settings.html',{'user_profile':user_profile})