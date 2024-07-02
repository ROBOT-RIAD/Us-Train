from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserLogoutView,UserAccountUpdateView,AddMoneyView,Activate

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('profile/',UserAccountUpdateView.as_view(),name='profile'),
    path('add-money/',AddMoneyView.as_view(),name ='add_money'),
    path('active/<uid64>/<token>/', Activate,name ='activate'),
]