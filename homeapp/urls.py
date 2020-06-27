
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home1,name="home1"),
    path('signup/',views.home,name="home"),
    path('home/',views.category,name="category"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path("<int:home_id>/", views.category_home, name='category_home'),
    path('profile/',views.profile_card,name="profile_card"),
    path('addwishlist/<int:home_id>/',views.addwishlist,name="wish_list"),
    path('removewishlist/<int:home_id>/',views.removewishlist,name="wish_list"),
    path('wishlist/',views.allwishlist,name="allwishlist"),
    path('yourhome/',views.yourhome,name="yourhome"),
    path('addhome/',views.addhome,name="addhome"),
    path('delete/<int:home_id>/',views.deletehome,name="deletehome"),
]

