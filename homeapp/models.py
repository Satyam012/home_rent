from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item", null=True)
    city = models.CharField(max_length=50)
    address =models.CharField(max_length=300)
    rent= models.IntegerField(null = True)
    description= models.CharField(max_length=500) 
    number=models.IntegerField(null=True)
    picture = models.FileField(blank=True, null=True)
    report =models.IntegerField(default=0)
    def __str__(self):
        return "Owner"+ self.user.username+ "-Location:"+ self.address + "-" + self.city
    
    
class extendedUser(models.Model):
    name= models.CharField(null=True,max_length=50,default= "...")
    image = models.FileField(null= True, default='user.png')
    email = models.CharField(null=True,default="...",max_length=50)
    phone_number = models.CharField(null= True,default="...",max_length=13)
    belongs_to = models.OneToOneField(User,related_name="extended_reverse",on_delete=models.CASCADE)
    home_list = models.ManyToManyField(Item,related_name="fav_home")
    def __str__(self):
        return  self.belongs_to.username +"'s wishList home"

          



