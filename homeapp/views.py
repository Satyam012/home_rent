from django.shortcuts import render,redirect
from .models import Item,extendedUser
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages
import math
from math import cos, sqrt
R = 6371000 #radius of the Earth in m
from math import radians, cos, sin, asin, sqrt 
def distance(lat1, lon1, lat2, lon2):
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 

    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))  

    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371

    # calculate the result 
    return(c * r) 
@login_required
def category(request):
    if 'getByCoordinate' in request.POST:
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        radius = float(request.POST['radius'])
        print(latitude,longitude,radius)
        all_houses = Item.objects.all()
        data = []
        for house in all_houses:
            if house.latitude and house.longitude and distance(house.latitude,house.longitude,latitude,longitude) <= radius:
                data.append(house)
    else:
        data = Item.objects.all()
        if 'search' in request.POST:
            city = request.POST['city']
            data = Item.objects.filter(city__contains = city )
    
    return render(request,'all_categories.html',{'all_category_objects':data})

def home(request):
    return render(request,'home.html')

def home1(request):
    return render(request,'home1.html')   

def login(request):#copied frm beat-connect master
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            messages.add_message(request, messages.INFO, 'Logged In')
            return redirect('/home/')
        else:
            messages.add_message(request, messages.INFO, 'Invalid Credential')
            return redirect('/')
            #return render(request, 'login.html', {'error_message': "Invalid Credentials"})
    #return render(request, 'login.html')
def register(request):
    if 'register' in request.POST:
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        username = request.POST['username']
        # age = request.POST['age']
        # number =request.POST['phone']
        image =request.FILES['image']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'home.html',{'error_message':"Username already taken"})
            else:
                user= User.objects.create_user(username = username, password = password1)
                user.save()
                my_extend_user = extendedUser(belongs_to= user,image=image )
                my_extend_user.save()
                return redirect('/')
        else:
            return render(request,'home.html',{'error_message':"Password does not match"})
    return render(request,'home.html') 

def category_home(request,home_id):
    home_card = Item.objects.get(id=home_id)
    return render(request,'home_card.html',{'home_card':home_card})

def profile_card(request,id):
    # extend_user_belongs_to = User.objects.get(id = id)
    userr= User.objects.get(id=id)
    return render(request,'profile.html',{'userr':userr})   

def addwishlist(request,home_id):#addding to wishlist code
    #return HttpResponse('okkkkkkkkk')
    home_card = Item.objects.get(id=home_id)
    extend_user_object = extendedUser.objects.get(belongs_to= request.user)
    extend_user_object.home_list.add(home_card)
    all_category_objects = Item.objects.all()
    print(request.user.extended_reverse.home_list.all())
    return render(request,'all_categories.html',{'all_category_objects':all_category_objects})

def removewishlist(request,home_id):
    home_card = Item.objects.get(id=home_id)
    extend_user_object = extendedUser.objects.get(belongs_to= request.user)
    extend_user_object.home_list.remove(home_card)
    all_category_objects = Item.objects.all()
    print(request.user.extended_reverse.home_list.all())
    return render(request,'all_categories.html',{'all_category_objects':all_category_objects})

@login_required
def allwishlist(request):
    extend_user_object = extendedUser.objects.get(belongs_to= request.user)
    return render(request,'wishlist.html',{'extend_user_object':extend_user_object})
@login_required
def allHomes(request,user_id):
    user_object= User.objects.get(id= user_id)
    all_object = Item.objects.filter(user= user_object)
    return render(request,'yourhome.html',{'all_object':all_object})   
@login_required
def yourhome(request):
    all_object = Item.objects.filter(user=request.user)
    return render(request,'yourhome.html',{'all_object':all_object})   

def addhome(request):    
    if 'submit' in request.POST:
        city = request.POST['city']
        address = request.POST['address']
        rent = request.POST['rent']
        number =request.POST['phone']
        image =request.FILES['image']
        description =request.POST['description']
        lat = float(request.POST['latitude'])
        lon = float(request.POST['longitude'])
        # bedroom1 =request.FILES['bedroom1']
        # bedroom2 =request.FILES['bedroom2']
        # kitchen =request.FILES['kitchen']
        # other =request.FILES['other']
        new_item= Item(user=request.user,city=city,address=address,rent=rent,number=number,description=description,picture=image,latitude = lat,longitude= lon)
        new_item.save()
        return redirect('/home/')
    return render(request,'addhome.html')
 
def deletehome(request,home_id):
     home_card = Item.objects.get(id=home_id)
     if home_card.user==request.user:
         home_card.delete()
         
     return redirect('/home/')    

def report(request,card_id):
     home_card = Item.objects.get(id=card_id)
     home_card.report=1   
     home_card.save()
     return render(request,'home_card.html',{'home_card':home_card})
  
@login_required     
def homerequest(request):
    if request.user.is_staff:
        home=Item.objects.filter(report=1)
        return render(request,'request.html',{'allhome':home})   
    else:
        raise Http404("You are not an admin")  

def accept(request,card_id):
    home_card = Item.objects.get(id=card_id)
    home_card.report=2  
    home_card.save() 
    return redirect('/request/')

def reject(request,card_id):
    home_card = Item.objects.get(id=card_id)
    home_card.report=0   
    home_card.save()
    return redirect('/request/')         