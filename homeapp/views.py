from django.shortcuts import render,redirect
from .models import Item,extendedUser
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages

@login_required
def category(request):
    all_category_objects = Item.objects.all()
    return render(request,'all_categories.html',{'all_category_objects':all_category_objects})

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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        age = request.POST['age']
        number =request.POST['phone']
        image =request.FILES['image']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'home.html',{'error_message':"Username already taken"})
            else:
                user= User.objects.create_user(username = username, password = password1, first_name= first_name, last_name = last_name)
                user.save()
                my_extend_user = extendedUser(belongs_to= user,phone_number=number,age=age,image=image )
                my_extend_user.save()
                return redirect('/')
        else:
            return render(request,'home.html',{'error_message':"Password does not match"})
    return render(request,'home.html') 

def category_home(request,home_id):
    home_card = Item.objects.get(id=home_id)
    return render(request,'home_card.html',{'home_card':home_card})

def profile_card(request):
    return render(request,'profile.html',{})   

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
        bedroom1 =request.FILES['bedroom1']
        bedroom2 =request.FILES['bedroom2']
        kitchen =request.FILES['kitchen']
        other =request.FILES['other']
        new_item= Item(user=request.user,city=city,address=address,rent=rent,number=number,description=description,picture=image,bedroom1=bedroom1,bedroom2=bedroom2,kitchen=kitchen,other=other)
        new_item.save()
        return redirect('/home/')
    return render(request,'addhome.html')
 
def deletehome(request,home_id):
     home_card = Item.objects.get(id=home_id)
     if home_card.user==request.user:
         home_card.delete()
         
     return redirect('/home/')    