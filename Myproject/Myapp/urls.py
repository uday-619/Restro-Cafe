from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index') ,
    path('menu/', views.menu, name='menu'),
    path('seat_reservation/',views.seat_reservation, name='seat_reservation'),
    path('contact/', views.contact, name='contact'),
    path('login_signup/', views.login_signup, name='login_signup'),
    path('logout/', views.logout_view, name='logout'),
    path('coffee/', views.coffee, name='coffee'),
]