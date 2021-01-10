from django.shortcuts import render,redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog_app.models import Post
from .forms import UpdateUserForm, UpdateProfileForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# ------------- show register form --------#
def registerform(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
                new_user= register_form.save(commit=False)
                password= register_form.cleaned_data['password1']
                username= register_form.cleaned_data['username']
                new_user.set_password(password)
                #new_user.password = password  #----wrong-- not work! 
                new_user.save()

                #-- to doing login automatically after register
                user = authenticate(username=username,password=password) # without(request)_only data
                login(request,user)
                #-----------
                messages.success(request,f'Congratulation ( {user.username} ) you register successfully and then login automatically :) ')
                register_form = RegisterForm()
                return redirect('account_app:profile')
    else:
        register_form = RegisterForm()
    
    context ={
        'form' : register_form ,
    }
    return render(request, 'account_app/register.html', context)
    



# ------------- show login form --------#
def loginform(request):
    if request.method =='POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        #print(username)-- work ok
        #print(password)-- work ok
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            login_form = LoginForm()
            messages.success(request, f'wellcome ( {user.username} ) :)')
            return redirect('blog_app:cats_list')
        else:
            login_form = LoginForm()
            messages.warning(request,'There is error in username or password,please try again')
            
            context = {
                'form': login_form,
            }
            return render(request, 'account_app/login.html', context)
       
    else:
        login_form = LoginForm()

        context ={
            'form': login_form,
        }
        return render(request,'account_app/login.html', context)








# ------------- show logoutform --------#
def logoutform(request):
    logout(request)
    messages.info(request, 'logout :(   waiting your login again ')
    return redirect('blog_app:cats_list')







# ------------- show profile form --------#
@login_required(login_url='account_app:login')

def profileform(request):
    posts_to_author = Post.objects.all().filter(post_author = request.user.id)
   
    #-- paginator --#
    paginator = Paginator(posts_to_author, 5)
    page = request.GET.get('page')
    try:
        posts_to_author = paginator.page(page)
    except PageNotAnInteger:
        posts_to_author = paginator.page(1)
    except EmptyPage:
        posts_to_author = paginator.page(paginator.num_page)
    
    context ={
        'page' : page ,
        'posts_to_author': posts_to_author ,
    }
    return render(request,'account_app/profile.html', context)
  






#   ----- update  (user form + profile form) at the same html form page ------# 
def updateuserprofile(request): 
    update_user_form = UpdateUserForm(instance= request.user)
    update_profile_form = UpdateProfileForm(instance= request.user.profile_to_user)
    
    if request.method == 'POST':
        update_user_form = UpdateUserForm(data= request.POST , instance= request.user)
        update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile_to_user)

        if update_user_form.is_valid and update_profile_form.is_valid :
            update_user_form.save()
            update_profile_form.save()
            messages.success(request,'your profile updated successfully..')
            return redirect('account_app:profile')
    
    else:
        update_user_form = UpdateUserForm(instance=request.user)
        update_profile_form = UpdateProfileForm(instance=request.user.profile_to_user)
    
    context ={
        'update_user_form': update_user_form ,
        'update_profile_form' : update_profile_form ,
    }
    return render(request,'account_app/update_user_profile.html',context)


