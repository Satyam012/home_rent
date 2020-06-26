
from django.urls import path,include
from . import views
app_name = 'home_app'
urlpatterns = [
    path('',views.home1,name="home1"),
    path('signup/',views.home,name="home"),
    path('home/',views.category,name="category"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path("<int:home_id>/", views.category_home, name='category_home'),
    path('profile/',views.profile_card,name="profile_card"),
    path('wishlist/<int:home_id>/',views.wish_list,name="wish_list"),
    path('wishlist/',views.allwishlist,name="allwishlist"),
]

