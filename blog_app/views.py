from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# ------------category------------------------------------------------------#
def cats_list(request):
    page_title = 'Categories'
    cats = Category.objects.all()
    #-- counter of categories --#
    cats_count = Category.objects.all().count()
    
    #-- paginator --#
    paginator = Paginator(cats, 5)
    page = request.GET.get('page')
    try:
        cats = paginator.page(page)
    except PageNotAnInteger:
        cats = paginator.page(1)
    except EmptyPage:
        cats = paginator.page(paginator.num_page)
    
    context = {
        'page' : page ,
        'page_title': page_title,
        'cats':cats,
        'cats_count': cats_count,
    }
    return render(request, 'blog_app/cats_list.html', context)



# ----------- same as cat dtail (need 1 args)--------------#
def posts_to_cat(request,cat_id):
    page_title = 'Posts to selected category'
    cat_selected = get_object_or_404(Category, id=cat_id)
    posts_cat = Post.objects.all().filter(cat_fk=cat_id)
    posts_cat_count = Post.objects.all().filter(cat_fk=cat_id).count() 
    
    #-- paginator --#
    paginator = Paginator(posts_cat, 3)
    page = request.GET.get('page')
    try:
        posts_cat = paginator.page(page)
    except PageNotAnInteger:
        posts_cat = paginator.page(1)
    except EmptyPage:
        posts_cat = paginator.page(paginator.num_page)

    
    context = {
        'page': page ,     
        'cat_selected': cat_selected,
        'posts_cat': posts_cat,
        'posts_cat_count': posts_cat_count,
        'page_title': page_title,
    }
    return render(request, 'blog_app/posts_to_category.html', context)



# ------------------need 2 args---------#
@login_required(login_url='account_app:login')

def cat_post_detail(request, cat_id, post_id):
    cat_selected = get_object_or_404(Category, id=cat_id)
    posts_cat = Post.objects.all().filter(cat_fk=cat_id)
    cat_post_detail = get_object_or_404(Post, cat_fk=cat_id, id=post_id, post_status='published')
   
    # to get views counter for selected post 
    session_key ='view_status_post_{}'.format(cat_post_detail.id)
    if not request.session.get(session_key,False):
       cat_post_detail.post_views_counter = cat_post_detail.post_views_counter+1
       cat_post_detail.save()
       request.session[session_key]=True


    #---to show comments for this post
    comments = Comment.objects.all().filter(post_fk= post_id)
    comments_post_count = Comment.objects.all().filter(post_fk=post_id).count()


    #---to show add comment form for this post -----#
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post_fk = cat_post_detail
            new_comment.comment_author = request.user
            new_comment.save()
            comment_form = CommentForm()
            messages.success(request,f'thanks ( {request.user.username} ),  new comment add successfully')
            return redirect('blog_app:cat_post_detail', cat_id=cat_selected.id, post_id=cat_post_detail.id)
           

            # #---- to get comments counter for this post
            # comments = Comment.objects.all().filter(post_fk= post_id)
            # comments_post_count = Comment.objects.all().filter(post_fk=post_id).count()        
    else:
        comment_form = CommentForm()
        
    context ={
        'cat_selected': cat_selected,
        'cat_post_detail': cat_post_detail,
        'comments': comments,
        'form': comment_form,
        'comments_post_count': comments_post_count,   
    }
    return render(request, 'blog_app/cat_post_detail.html', context)



# -------------------------------------------#
@login_required(login_url='account_app:login')

def post_add(request,cat_id):
    cat_selected = get_object_or_404(Category, id=cat_id)
    
    # --- to get posts counter for this category 
    posts_cat = Post.objects.all().filter(cat_fk=cat_id)
    posts_cat_count = Post.objects.all().filter(cat_fk=cat_id).count()
    
    # -- add new post form 
    if request.method=='POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.cat_fk = cat_selected
            new_post.post_author = request.user
            new_post.save()
            post_form = PostForm()
            messages.success(
            request, f'thanks ( {request.user.username} ),new post add successfully')
            return redirect('blog_app:posts_to_cat', cat_id=cat_selected.id)
    else:
        post_form = PostForm()
    context = {
        'cat_selected': cat_selected,
        'posts_cat_count' : posts_cat_count ,
        'form' : post_form,

    }
    return render(request, 'blog_app/post_add.html', context)
# -------------------------#


#--- post update -----------#
@login_required(login_url='account_app:login')

def post_update(request, cat_id, post_id):
    cat_selected = get_object_or_404(Category, id=cat_id)
    posts_cat = Post.objects.all().filter(cat_fk=cat_id)
    cat_post_detail = get_object_or_404(Post, cat_fk=cat_id, id=post_id, post_status='published')
    
    post_form = PostForm(request.POST or None,
                         request.FILES or None,
                         instance=cat_post_detail)
    if post_form.is_valid():
        new_post= post_form.save(commit=False)
        new_post.cat_fk = cat_selected
        new_post.post_author = request.user
        new_post.save()
        messages.success(request, f'thanks ( {request.user.username} ),the post updated successfully')
        return redirect('blog_app:cat_post_detail', cat_id=cat_selected.id, post_id=cat_post_detail.id)
    
    context ={
        'form' : post_form,
        'cat_selected': cat_selected,
        'cat_post_detail': cat_post_detail,
    }
    return render(request, 'blog_app/post_update.html', context)








#--- post delete -----------#
@login_required(login_url='account_app:login')

def post_delete(request, cat_id, post_id):
    cat_selected = get_object_or_404(Category, id=cat_id)
    posts_cat = Post.objects.all().filter(cat_fk=cat_id)
    cat_post_detail = get_object_or_404(Post, cat_fk=cat_id, id=post_id, post_status='published')
    
    if request.method =='POST':
        cat_post_detail.delete()
        messages.success(request, f'thanks ( {request.user.username} ), post deleted successfully')
        return redirect('blog_app:posts_to_cat', cat_id=cat_selected.id)

    context ={
        'cat_selected': cat_selected,
        'cat_post_detail': cat_post_detail,
    }
    return render(request,'blog_app/post_delete.html',context)















# ---------- not need ---------------#
# def cat_detail(request,cat_id):
#     cat_detail = get_object_or_404(Category, id=cat_id)
#     context = {
#         'cat_detail': cat_detail ,
#     }
#     return render(request, 'blog_app/cat_detail.html', context)


# -------------------------# not need _ _only admin can add new cat in admin page
# def cats_add(request):
#     context = {

#     }
#     return render(request, 'blog_app/cats_add.html', context)


# ------------all posts -- not need  ------------------------#
# def all_posts_list(request):
#     posts = Post.objects.all()
#     page_title = 'Posts'
#     context = {
#         'posts': posts,
#         'page_title': page_title,
#     }
#     return render(request, 'blog_app/posts_list.html', context)
