from django.shortcuts import render,redirect
from .models import Item,extendedUser
from django.http import HttpResponse,Http404
import http.client
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login
import random
from django.core.mail import send_mail
#-----------------------------forget password------------------------------
def mail(username,email,otp):  
    subject = "verification for home_Rent website"  
    msg     = "Hi "+username+',\n\nwe have received your sign-up request\n <#>Your Home-rent\'s login OTP is '+otp
    to      = email
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  

def set_password(request):
    if 'submit' in request.POST:
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
                user = User.objects.get(username=request.session['username'])
                user.set_password(password1)

                user.save()
                return redirect('/')
        else:
            return render(request,'set_password.html',{'message':"Password does not match"})

    return render(request,'set_password.html')

def forget(request):
    if 'submit' in request.POST:
        username = request.POST['username']
        if User.objects.filter(username = username).exists():
            user = User.objects.get(username=username)
            profile= extendedUser.objects.get(belongs_to=user)
            email=profile.email
            otp=str(random.randint(1000,9999))
            mail(username,email,otp)
            request.session['otp'] = otp
            request.session['username'] = username
            return render(request, 'otp.html', {'reset':'reset'})
        else:
            return render(request, 'forget.html', {'message': "Invalid Username*"})
        
        
    return render(request,'forget.html')


#-------------------------------signup page---------------------------------------------



def register(request):
    if 'register' in request.POST:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'signup.html',{'message':"Username already taken*"})
            else:
                otp=str(random.randint(1000,9999))
                request.session['username'] = username
                request.session['password'] = password1
                request.session['email'] = email
                request.session['otp'] = otp
                mail(username,email,otp)
                return render(request, 'otp.html', {'register':'register'})
        else:
            return render(request,'signup.html',{'message':"Password does not match"})

    return render(request,'signup.html')         

def otp_submit(request):

    if 'otp_reset' in request.POST:        #for password reset
        otp=request.POST['otp_number']   

        if otp==request.session['otp']:
            return redirect('/set_password')
        else:
            return render(request,'otp.html',{'message':"wrong otp"}) 
        

    if 'otp_submit' in request.POST:    #for create new account
        otp=request.POST['otp_number']   

        if otp==request.session['otp']:
            user= User.objects.create_user(username = request.session['username'], password = request.session['password'])
            user.save()
            my_extend_user = extendedUser(belongs_to= user,email=request.session['email'],name=request.session['username'])
            my_extend_user.save()
            return redirect('/')
        else:
            return render(request,'otp.html',{'message':"wrong otp"}) 
    return render(request,'otp.html') 

# -------------------------------login page---------------------------------------------

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
            return render(request, 'login.html', {'message': "Invalid Credentials*"})

    if not request.user.is_authenticated:
        return render(request,'login.html')
    else:
        return redirect('/home')


# -----------------------------for home page-----------------------------------------
@login_required
def category(request):
    data = Item.objects.all()
    return render(request,'all_categories.html',{'all_category_objects':data})


#------------------------------For home card---------------------------------------------
@login_required
def category_home(request,home_id):
    home_card = Item.objects.get(id=home_id)
    return render(request,'home_card.html',{'home_card':home_card})


#-------------------------------for wishlist---------------------------------------------------
@login_required
def addwishlist(request,home_id):#addding to wishlist code
    home_card = Item.objects.get(id=home_id)
    extend_user_object = extendedUser.objects.get(belongs_to= request.user)
    extend_user_object.home_list.add(home_card)
    all_category_objects = Item.objects.all()
    print(request.user.extended_reverse.home_list.all())
    return render(request,'all_categories.html',{'all_category_objects':all_category_objects})

@login_required
def removewishlist(request,home_id):
    home_card = Item.objects.get(id=home_id)
    extend_user_object = extendedUser.objects.get(belongs_to= request.user)
    extend_user_object.home_list.remove(home_card)
    return redirect('/wishlist/')

@login_required
def allwishlist(request):
    extend_user_object = extendedUser.objects.get(belongs_to= request.user)
    return render(request,'wishlist.html',{'extend_user_object':extend_user_object})


# ----------------------------------for your home-----------------------------------
    

@login_required
def yourhome(request):
    all_object = Item.objects.filter(user=request.user)
    return render(request,'yourhome.html',{'all_object':all_object})   
 

@login_required
def deletehome(request,home_id):
     home_card = Item.objects.get(id=home_id)
     if home_card.user==request.user:
         home_card.delete()
     return redirect('/yourhome/')  

@login_required
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


# --------------------------------add home---------------------------------------------------
@login_required
def addhome(request):    
    if 'submit' in request.POST:
        city = request.POST['city']
        address = request.POST['address']
        rent = request.POST['rent']
        number =request.POST['phone']
        image =request.FILES['image']
        description =request.POST['description']
        status= request.POST['availability']
        new_item= Item(user=request.user,city=city,address=address,rent=rent,number=number,description=description,picture=image,availability=status)
        new_item.save()
        return redirect('/home/')
    return render(request,'addhome.html')


#-------------------------------about page--------------------------------------------------
@login_required
def about(request):
    return render(request,'about.html')  



#------------------------------for profile-----------------------------------------------------
@login_required  
def profile_card(request,id):
    userr= User.objects.get(id=id)
    profile= extendedUser.objects.get(belongs_to=userr)
    return render(request,'profile.html',{'obj':profile})   

@login_required  
def editprofile(request,profile_id):
    profile = extendedUser.objects.get(id=profile_id)
    if 'submit' in request.POST:
        profile.name= request.POST['name']
        profile.email = request.POST['email']
        profile.phone_number = request.POST['phone']
        profile.image =request.FILES['image']
        profile.save()
        ss = profile.belongs_to.id
        return redirect('/profile/'+str(ss)+'/')  
    return render(request,'editprofile.html',{'obj':profile})


#-------------------------------Reported home for admin-------------------------------------  

@login_required  
def report(request,card_id):
    home_card = Item.objects.get(id=card_id)
    home_card.report=1+abs(home_card.report)   
    status=home_card.status
    home_card.save()
    return render(request,'home_card.html',{'home_card':home_card,'status':status})

@login_required     
def homerequest(request):
    if request.user.is_staff:
        home=Item.objects.filter(report__gte =1)
        return render(request,'request.html',{'allhome':home})   
    else:
        raise Http404("You are not an admin")  

@login_required  
def accept(request,card_id):
    if request.user.is_staff:
        home_card = Item.objects.get(id=card_id)
        home_card.status="NOT SAFE"
        home_card.report*=(-1);  
        home_card.save() 
        return redirect('/request/')
    else:
        raise Http404("You are not an admin") 

@login_required  
def reject(request,card_id):
    if request.user.is_staff:
        home_card = Item.objects.get(id=card_id)
        home_card.report=0   
        home_card.status="SAFE"
        home_card.save()
        return redirect('/request/')         
    else:
        raise Http404("You are not an admin") 

@login_required  
def block(request,card_id):
    if request.user.is_staff:
        home_card = Item.objects.get(id=card_id)
        home_card.delete()
        return redirect('/request/') 
    else:
        raise Http404("You are not an admin")     

# -------------------------------------------------------------------

# @login_required                                           #for all home list of a perticular user
# def allHomes(request,user_id):
#     user_object= User.objects.get(id= user_id)
#     all_object = Item.objects.filter(user= user_object)
#     return render(request,'yourhome.html',{'all_object':all_object})   
