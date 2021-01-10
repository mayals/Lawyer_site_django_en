from django.urls import path
from. import views

app_name = 'account_app'
urlpatterns =[
    path('register/',views.registerform,name='register'),
    path('login/',views.loginform,name='login'),
    path('logout/',views.logoutform,name='logout'),
    path('profile/',views.profileform,name='profile'),
    path('update_user_profile/', views.updateuserprofile, name='update_user_profile'),
]

