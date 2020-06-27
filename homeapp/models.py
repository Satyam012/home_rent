from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.

class Image(models.Model):
    image = models.FileField()
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item", null=True)
    city = models.CharField(max_length=50)
    address =models.CharField(max_length=300)
    latitude = models.IntegerField(null=True,blank=False)
    longitude = models.IntegerField(null=True,blank=False)
    rent= models.IntegerField(null = True)
    description= models.CharField(max_length=500) 
    number=models.IntegerField(null=True)
    picture = models.FileField(null=True)
    kitchen = models.FileField(blank=True, null=True)   
    bedroom1 = models.FileField(blank=True, null=True)   
    bedroom2 = models.FileField(blank=True, null=True)
    other = models.FileField(blank=True, null=True) 
    
class extendedUser(models.Model):
    age = models.IntegerField(null=True)
    image = models.FileField(null= True)
    phone_number = models.IntegerField(null= True)
    belongs_to = models.OneToOneField(User,related_name="extended_reverse",on_delete=models.CASCADE)
    home_list = models.ManyToManyField(Item,related_name="fav_home")
    def __str__(self):
        return  self.belongs_to.username +"'s wishList home"

          



