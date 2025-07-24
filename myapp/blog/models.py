from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


#Category
class Categorie(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  image_url = models.ImageField(null=True, upload_to="posts/images")
  created_at = models.DateTimeField(auto_now_add=True)
  slug = models.SlugField(default='example-slug', unique=True)
  category = models.ForeignKey(Categorie,on_delete=models.CASCADE)
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  is_published = models.BooleanField(default=False)

  def save(self,*args, **kwargs):
    self.slug = slugify(self.title)
    super().save(*args, **kwargs)

  @property
  def formatted_img_url(self):
    url = self.image_url if self.image_url.__str__().startswith(('http://','https://')) else self.image_url.url
    return url

  def __str__(self):
    return self.title


class AboutUs(models.Model):
  content = models.TextField()
