from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("login",views.user_login,name="login"),
    path("signup",views.user_signup,name="signup"),
    path("logout",views.user_logout,name="logout"),
    path("myfiles",views.myfiles,name="myfiles"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]