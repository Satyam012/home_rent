from django.shortcuts import render,redirect
from .models import Item,extendedUser
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages

@login_required
def category(request):
    print('satyam')
    data = Item.objects.all()
    if 'search' in request.POST:
        city = request.POST['city']
        data = Item.objects.filter(city__contains = city )
    
    return render(request,'all_categories.html',{'all_category_objects':data})
#signup page
def home(request):
    return render(request,'home.html')

#login page
def home1(request):
    if not request.user.is_authenticated:
        return render(request,'home1.html')
    else:
        return redirect('/home')

def login(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            messages.add_message(request, messages.INFO, 'Logged In')
            return redirect('/home/')
        else:
            return render(request, 'home1.html', {'message': "Invalid Credentials*"})

def register(request):
    if 'register' in request.POST:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'home.html',{'message':"Username already taken*"})
            else:
                user= User.objects.create_user(username = username, password = password1)
                user.save()
                my_extend_user = extendedUser(belongs_to= user)
                my_extend_user.save()
                return redirect('/')
        else:
            return render(request,'home.html',{'message':"Password does not match"})
    return render(request,'home.html') 

def category_home(request,home_id):
    home_card = Item.objects.get(id=home_id)
    return render(request,'home_card.html',{'home_card':home_card})

def profile_card(request,id):
    userr= User.objects.get(id=id)
    profile= extendedUser.objects.get(belongs_to=userr)
    return render(request,'profile.html',{'obj':profile})   

def addwishlist(request,home_id):#addding to wishlist code
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
        new_item= Item(user=request.user,city=city,address=address,rent=rent,number=number,description=description,picture=image)
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

def about(request):
    return render(request,'about.html')    

def edit(request,home_id):
    home_card = Item.objects.get(id=home_id)
    if 'submit' in request.POST:
        obj=Item.objects.get(id=home_id)
        obj.city = request.POST['city']
        obj.address = request.POST['address']
        obj.rent = request.POST['rent']
        obj.number =request.POST['phone']
        obj.description =request.POST['description']
        obj.save()
        return redirect('/yourhome/')
    return render(request,'edithome.html',{'obj':home_card})

def editprofile(request,profile_id):
    profile = extendedUser.objects.get(id=profile_id)
    if 'submit' in request.POST:
        profile.name= request.POST['name']
        profile.email = request.POST['email']
        profile.phone = request.POST['phone']
        profile.image =request.FILES['image']
        profile.save()
        ss = profile.belongs_to.id
        return redirect('/profile/'+str(ss)+'/')  
    return render(request,'editprofile.html',{'obj':profile})