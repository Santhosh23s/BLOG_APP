from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import Http404
from .models import Categorie, Post,AboutUs
from django.core.paginator import Paginator
from .forms import ContactForm, ForgotPassword, LoginForm, PostForm,RegisterForm,ResetPasswordUser
import logging
from django.contrib import messages # This is used to show the success message 
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group
# Create your views here.
# This is the data of constant
# posts = [
#   {'id':1,'title':'Post 1', 'content':'This is the content of post 1'},
#   {'id':2,'title':'Post 2', 'content':'This is the content of post 2'},
#   {'id':3,'title':'Post 3', 'content':'This is the content of post 3'},
#   {'id':4,'title':'Post 4','content':'This is the content of post 4'},
# ]


def index(request):
  blog_title ="Latest Post"
  # This is the method to get all the details 
  all_posts = Post.objects.filter(is_published=True)
  #We want to make it as paginator
  paginator = Paginator(all_posts,5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request,'blog/index.html',{'blog_title':blog_title,'page_obj': page_obj});

def postDetail(request,slug):

  if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request, 'You have no permission to view any posts')
        return redirect('blog:index')
  # This is the constant method to retrieve post from the local db 
  # post = next((item for item in posts if item['id'] == postId),None)
  # This is used for debugging 
  # logger = logging.getLogger("TESTING")
  # logger.debug(f'The Post ID is {post}')
  # This is make to put in try block bcoz if error happend we want to handle it so...

  # if request.user and not request.user.has_perm('blog.view_post'):
  #   messages.ERROR(request,"You have no Permisson to view Posts!Sorry Try Again Later")
  #   return redirect(request,'blog:index')

  try:
    # This would handle the error if the post does not exist
    post = Post.objects.get(slug=slug)
    related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)

  except Post.DoesNotExist:
    # If post does not available it will handle it ....
    raise Http404("Post Does Not Exist!")
  
  return render(request,'blog/detail.html',{'post':post,'related_posts':related_posts});

def oldUrlRedirect(request):
  return redirect(reverse("blog:newUrlFun"));

def newUrl(request):
  return HttpResponse("This is redirected from the old url");

def contact(request):
  if request.method == 'POST':
   form = ContactForm(request.POST)
   name = request.POST.get('name')
   email = request.POST.get('email')
   message = request.POST.get('message')
   logger = logging.getLogger("TESTING")
   if form.is_valid():
    logger.debug(f'The POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
    success_message = 'Your Email Is Sent message !'
    return render(request,'blog/contact.html',{'form':form ,'success_message':success_message})
   else:
    logger.debug("Form Validation Is Failure!")
   return render(request,'blog/contact.html',{'form':form ,'name':name,'email':email,'message':message})
  return render(request,'blog/contact.html')

def about(request):
  about_content = AboutUs.objects.first()
  if about_content is None or not about_content.content:
    about_content = "This is the Default About if the about is not Loaded Properly!"
  else:
    about_content = about_content.content
  return render(request,'blog/about.html',{'about_content':about_content})

def register(request):
  form = RegisterForm()
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False) # Creating the user data
      user.set_password(form.cleaned_data['password']) # This is the way to make the password hasing for the security purpose !
      user.save()
      # Here All The New Registers Are Defaultly added too default group
      register_group,created = Group.objects.get_or_create(name="Readers")
      user.groups.add(register_group)
      print("Register Form Submitted SuccessFully!")
      messages.success(request,"Registration Successful!You Can Login")
      return redirect("blog:login")

  return render(request,'blog/register.html',{'form':form})

def login(request):
  form = LoginForm()
  if request.method == "POST":
    # Login Form 
    form = LoginForm(request.POST)
    if form.is_valid():
     username = form.cleaned_data['username']
     password = form.cleaned_data['password']
     user = authenticate(username=username,password=password)
     if user is not None:
       auth_login(request,user)
       return redirect("blog:dashboard") # Redirect to Dashboard
     print("LOGIN SUCCESS!")
  return render(request,'blog/login.html',{'form':form})

def dashboard(request):
  blog_title = "My Posts"
  # Getting All Post
  all_posts = Post.objects.filter(user=request.user)
  paginator = Paginator(all_posts,5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request,'blog/dashboard.html',{"blog_title":blog_title,'page_obj':page_obj})

def logout(request):
  auth_logout(request)
  return redirect("blog:index")


def forgot_password(request):
  form = ForgotPassword()
  if request.method == 'POST':
    form = ForgotPassword(request.POST)

    if form.is_valid():
      email = form.cleaned_data['email']
      user = User.objects.get(email=email)

      token = default_token_generator.make_token(user)
      uid = urlsafe_base64_encode(force_bytes(user.pk))
      current_site = get_current_site(request)
      domain = current_site.domain

      subject="Request For ResetPassword!"
      message = render_to_string('blog/password_reset_email.html',{
        'domain':domain,
        'uid':uid,
        'token':token
      })
      send_mail(subject,message,'noreply@sandev.com',[email])
      messages.success(request,"Email Code is Sent!")
  return render(request,'blog/forgot_password.html',{'form':form})

def reset_password(request,uidb64,token):
  form = ResetPasswordUser()
  if request.method == 'POST':
    # Form 
    form = ResetPasswordUser(request.POST)
    if form.is_valid():
      new_password = form.cleaned_data['new_password']
      try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
      except (TypeError,ValueError,User.DoesNotExist):
        user = None

      if user is not None and default_token_generator.check_token(user,token):
        user.set_password(new_password)
        user.save()
        messages.success(request,"The Password Is reseted!Back to login")
        return redirect('blog:login')
      else:
        messages.error(request,"The Password Reset Link Is Invalid")
      
  return render(request,'blog/reset_password.html',{'form':form})

@login_required
@permission_required('blog.add_post',raise_exception=True)
def new_post(request):
  categories = Categorie.objects.all()
  form = PostForm()
  if request.method == 'POST':
    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
      return redirect("blog:dashboard")
  return render(request,'blog/new_post.html',{'categories':categories,'form':form})

@login_required
@permission_required('blog.change_post',raise_exception=True)
def edit_post(request,post_id):
  categories = Categorie.objects.all()
  post = get_object_or_404(Post, id=post_id)
  form = PostForm()

  if request.method == 'POST':
    form = PostForm(request.POST,request.FILES,instance=post)
    if form.is_valid():
      form.save()
      messages.success(request,"Post Updated SuccessFully!")
      return redirect('blog:dashboard')
  

  return render(request,'blog/edit_post.html',{'categories':categories,'post':post,'form':form})

@login_required
@permission_required('blog.delete_post',raise_exception=True)
def delete_post(request,post_id):
  post = get_object_or_404(Post, id=post_id)
  post.delete()
  messages.success(request,"Post Deleted SuccessFully!")
  return redirect('blog:dashboard')

@login_required
@permission_required('blog.can_publish',raise_exception=True)
def publish_post(request,post_id):
  post = get_object_or_404(Post, id=post_id)
  post.is_published = True
  post.save()
  messages.success(request,"Post Published SuccessFully!")
  return redirect('blog:dashboard')