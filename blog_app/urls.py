from django.urls import path
from .import views


app_name = 'blog_app'
urlpatterns =[
    path('cats_list/', views.cats_list, name='cats_list'),
    path('posts_to_cat/<slug:cat_id>/', views.posts_to_cat, name='posts_to_cat'),
    path('posts_to_cat/<slug:cat_id>/post_add/',views.post_add, name='post_add'),  
    path('posts_to_cat/<slug:cat_id>/post_detail/<slug:post_id>/',views.cat_post_detail, name='cat_post_detail'),
    path('posts_to_cat/<slug:cat_id>/post_detail/<slug:post_id>/update/',views.post_update, name='post_update'),
    path('posts_to_cat/<slug:cat_id>/post_detail/<slug:post_id>/delete/',views.post_delete, name='post_delete'),
   
    #path('cat_add/', views.cats_add, name='cat_add'),#not need
    # path('cat_detail/<slug:cat_id>/', views.cat_detail, name='cat_detail'), #not need
    # path('all_posts_list/', views.all_posts_list, name='all_posts_list'),#not need
]
