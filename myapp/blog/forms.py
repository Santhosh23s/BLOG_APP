from multiprocessing import AuthenticationError
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Categorie, Post

class ContactForm(forms.Form):
  name = forms.CharField(label='Name',max_length=100,required=True)
  email = forms.EmailField(label='Email',required=True)
  message = forms.CharField(label='Message', required=True)

class RegisterForm(forms.ModelForm):
  username = forms.CharField(label='UserName',max_length=100,required=True)
  email = forms.EmailField(label='Email',max_length=100,required=True)
  password = forms.CharField(label='Password',max_length=100,required=True)
  password_confirm = forms.CharField(label='ConfirmPassword',max_length=100,required=True)

  class Meta:
    model = User
    fields = ['username','email','password']

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    password_confirm = cleaned_data.get('password_confirm')
    if password and password_confirm and password != password_confirm:
      raise forms.ValidationError("Password Does Not Match! Enter The Correct Password!")
    

class LoginForm(forms.Form):
  username = forms.CharField(label='username',max_length=100,required=True)
  password = forms.CharField(label='passworrd',max_length=100,required=True)

  def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get("username")
    password = cleaned_data.get("password")

    if username and password:
      user = authenticate(username=username,password=password)
      if user is None:
        raise forms.ValidationError("Invalid Username Or Password!")

class ForgotPassword(forms.Form):
  email = forms.EmailField(label="Email",max_length=254,required=True)

  def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')

    if not User.objects.filter(email=email).exists():
      raise forms.ValidationError("The User Is Not Found.Create and Register an Account!")
    

class ResetPasswordUser(forms.Form):
  new_password = forms.CharField(label='New Password',min_length=8)
  confirm_password = forms.CharField(label='Confirm Password',min_length=8) 

  def clean(self):
    cleaned_data = super().clean()
    new_password = cleaned_data.get('new_password')
    confirm_password = cleaned_data.get('confirm_password')

    if new_password and confirm_password and new_password != confirm_password:
      raise forms.ValidationError("Password Does Not Match! Enter The Correct Password!")



class PostForm(forms.ModelForm):
  title = forms.CharField(label="Name",max_length=200,required=True)  
  content = forms.CharField(label="Content",required=True)
  category = forms.ModelChoiceField(label="Category",required=True,queryset=Categorie.objects.all())
  image_url = forms.ImageField(label="Image",required=False)

  class Meta:
    model = Post
    fields = [
      'title',
      'content',
      'category',
      'image_url'
    ] 

  def clean(self):
    cleaned_data =  super().clean()
    title = cleaned_data.get('title')
    content = cleaned_data.get('content')
    image_url = cleaned_data.get('image_url')

    #Condition
    if title and len(title)<5:
      raise forms.ValidationError("The Title length must be greater than 5")
    #Condition for content
    if content and len(content)<10:
      raise forms.ValidationError("The Content length Must be greater than 10")


  def save(self, commit = ...):
    post = super().save(commit)
    cleaned_data =  super().clean()

    if cleaned_data.get('image_url'):
      post.image_url = cleaned_data.get('image_url')
    
    else:
      img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"
      post.image_url = img_url

    if commit:
      post.save()
    return post