from typing import Any
from blog.models import Categorie
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  help = "Populate the database with categorie data"
  def handle(self, *args, **options):
    # This command is used to delete all the data from the db
    Categorie.objects.all().delete()

    categories = [
      'Sports',
      'Technology',
      'Science',
      'Art',
      'Food'
    ]
    for categorie_name in categories:
      Categorie.objects.create(name=categorie_name)

    self.stdout.write(self.style.SUCCESS("The Demo Data Is Inserted in DataBase Succesfull!"))