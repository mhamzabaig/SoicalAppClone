from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Post,LikePost,FollowersCount
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from itertools import chain
import random
# Create your views here.

@login_required(login_url='/signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)\
        
    

    new_suggestion = [x for x in list(all_users) if (x not in list(user_following_all))]
    
    current = User.objects.filter(username= request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion) if (x not in list(current))]

    random.shuffle(final_suggestion_list)
    username_profile= []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)

    suggestion_username_profile_list = list(chain(*username_profile_list))

    print(username_profile_list)
    

    return render(request,'index.html',{'user_profile':user_profile,'posts':feed_list,'suggestion_username_profile_list':suggestion_username_profile_list})

@login_required(login_url='/signin')
def search(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        user_profile = []
        user_profile_list = []

        for users in username_object:
            user_profile.append(users.id)
        for ids in user_profile:
            profile_obj = Profile.objects.filter(user_id = ids)
            user_profile_list.append(profile_obj)
        print(user_profile_list)
        user_profile_list = list(chain(*user_profile_list))
        
        print(user_profile_list)

    return render(request,'search.html',{'user_profile':user_profile,'user_profile_list':user_profile_list})

@login_required(login_url='/signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    # Checking if same user has liked a single post more than once
    like_filter = LikePost.objects.filter(post_id=post_id,username=username)
    
    if len(like_filter) == 0:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes  += 1
        post.save()
    elif len(like_filter) and post.no_of_likes>0:
        like_filter.delete()
        post.no_of_likes -=  1
        post.save()
    return redirect('/')

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

@login_required(login_url='/signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_len = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_posts_len':user_posts_len,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following
    }
    return render(request,'profile.html',context)

@login_required(login_url='/signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower,user=user):
            delete_follower = FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
        else:
            new_follower = FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
        return redirect('/profile/' + user)
    else:
        return redirect('/')

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
        return redirect('/')    
    
    return render(request,'settings.html',{'user_profile':user_profile})