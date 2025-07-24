from django.urls import reverse
from django.shortcuts import redirect

class RequestHandlerOnMiddleWare:
  def __init__(self,get_response):
    self.get_response = get_response
  def __call__(self,request):
    # Check the user is autheticated
    if request.user.is_authenticated:
      # List the path to check
      paths_to_redirect = [reverse('blog:login'),reverse('blog:register')]
      # To verify the user paths
      if request.path in paths_to_redirect:
        return redirect(reverse('blog:index')) # path to change
      
    response = self.get_response(request)
    return response
  
class RedirectIfNotLogin:
  def __init__(self,get_response):
    self.get_response = get_response
  def __call__(self,request):
    restricted_paths =[reverse('blog:dashboard')]

    if not request.user.is_authenticated and request.path in restricted_paths:
      return redirect(reverse('blog:login'))
    
    response = self.get_response(request)
    return response