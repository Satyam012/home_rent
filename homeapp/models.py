from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item", null=True)
    city = models.CharField(max_length=50)
    address =models.CharField(max_length=300)
    rent= models.IntegerField(null = True)
    description= models.CharField(max_length=500) 
    number=models.IntegerField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    picture = models.FileField(blank=True, null=True)
    report =models.IntegerField(default=0)
    status =models.CharField(max_length=50,default="Safe") 
    availability = models.CharField(max_length=200, default="Available")  
    def __str__(self):
        return "Location:"+ self.address + "-" + self.city
    
    
class extendedUser(models.Model):
    name= models.CharField(null=True,max_length=50,default= "...")
    is_verified = models.BooleanField(default=False)
    otp_key = models.CharField(max_length=20,null=True)
    otp_created_time = models.DateTimeField(null=True)
    otp_used_count = models.IntegerField(default=0)
    image = models.FileField(null= True, default='user.png')
    email = models.CharField(null=True,default="...",max_length=50)
    phone_number=models.CharField(null=True,max_length=12)
    belongs_to = models.OneToOneField(User,related_name="extended_reverse",on_delete=models.CASCADE)
    home_list = models.ManyToManyField(Item,related_name="fav_home")
    def __str__(self):
        return  self.belongs_to.username +"'s Profile"

          



