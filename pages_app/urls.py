from django.urls import path,include
from . import views

app_name = 'pages_app'
urlpatterns = [
    path('',views.index, name ='index'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('service/', views.service, name='service'),
    path('contact/', views.contactus, name='contactus'),
    path('success_contactus/', views.success_contactus, name='success_contactus'),
    path('under_construction/', views.under_construction, name='under_construction')
]
