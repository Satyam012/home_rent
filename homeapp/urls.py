
from django.urls import path,include
from . import views
app_name = 'home_app'
urlpatterns = [
    path('',views.login,name="login"),
    path('signup/',views.register,name="signup"),
    path('home/',views.category,name="category"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path("<int:home_id>/", views.category_home, name='category_home'),
    path('profile/<int:id>/',views.profile_card,name="profile_card"),
    path('addwishlist/<int:home_id>/',views.addwishlist,name="wish_list"),
    path('removewishlist/<int:home_id>/',views.removewishlist,name="wish_list"),
    path('wishlist/',views.allwishlist,name="allwishlist"),
    path('yourhome/',views.yourhome,name="yourhome"),
    path('addhome/',views.addhome,name="addhome"),
    path('delete/<int:home_id>/',views.deletehome,name="deletehome"),
    path('report/<int:card_id>/',views.report,name="reporthome"),
    path('request/',views.homerequest,name="homerequest"),
    path('accept/<int:card_id>/',views.accept,name="accept"),
    path('reject/<int:card_id>/',views.reject,name="reject"),
    # path('allHome/<int:user_id>/',views.allHomes,name="allHomes"),
    path('block/<int:card_id>/',views.block,name="block"),
    path('about/',views.about),
    path('edit/<int:home_id>/',views.edit),
    path('editprofile/<int:profile_id>/',views.editprofile),
    path('otp/',views.otp_submit),
    path('forget/',views.forget),
    path('set_password/',views.set_password),
    path('filter_home/<str:home_name>/',views.FilterHome,name='filer_home'),
]

