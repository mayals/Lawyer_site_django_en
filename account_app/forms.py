from django.contrib.auth.models import User
from .models import Profile
from django import forms


# ----------register form ---------------------#
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=30, required=True,help_text='No space allowed')
    first_name = forms.CharField(label='first name', max_length=30, required=True)
    last_name  = forms.CharField(label='last name', max_length=30, required=False)
    email = forms.CharField(label='E-Mail', max_length=100, required=True)
    password1 = forms.CharField(label='password', min_length=6, required=True,help_text='use 6 and more', widget=forms.PasswordInput())
    password2 = forms.CharField(label='password configration', min_length=6,required=True, help_text='use 6 and more', widget=forms.PasswordInput())
#----- to costumize the RegisterForm fields -----# 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
# ------- to check that password2 equal password1 -----#
    def clean_password2(self):
         if  self.cleaned_data['password1']!= self.cleaned_data['password2']:
            raise forms.ValidationError('Error!!! the passwords not equal !')
         return self.cleaned_data['password2']
# ------- to check that username (unique) not used before -----#
    def clean_username(self):
        if User.objects.filter(username = self.cleaned_data['username']).exists():
            raise forms.ValidationError('Sorry you can not use it,this username has used before !!')
        return self.cleaned_data['username']






# ----------login form ---------------------#
class LoginForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=30, required=True)
    password = forms.CharField(label='password', min_length=6, required=True, widget=forms.PasswordInput())  

#----- to costumize the LoginForm fields -----#   
    class Meta:
        model = User
        fields = ['username','password']







#--- the next two update class forms will put in the same view fhunction __ and display in the same html form--

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(label='first name', max_length=30, required=True)
    last_name  = forms.CharField(label='last name', max_length=30, required=False)
    email = forms.CharField(label='Email', max_length=100, required=True, disabled=False)
    email = forms.CharField(label='E-Mail', max_length=100, required=True)
    
    class Meta:
        model = User
        #fields = ('_all_',) -- not work in one to one relationship !!
        fields = ['first_name','last_name','email']


class UpdateProfileForm(forms.ModelForm):
   
    class Meta:
        model = Profile
        #fields = ('_all_',)-- not work in one to one relationship !!
        fields = ['prof_image','prof_mob', 'gender']


#----------------------------------------------------------------------------
