from django.contrib import admin
from django.urls import path
from account import views

admin.site.site_header = "CDC ADMIN"
admin.site.site_title = "CDC ADMIN"
admin.site.index_title = "CDC ADMIN"

urlpatterns = [
   path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('student/', views.student, name='student'),
    path('teacher/', views.teacher, name='teacher'),
    path('cdc/', views.cdc, name='cdc'),
    path('addnews/', views.addnews, name='addnews'),
    path('allnews/', views.allnews, name='allnews'),
    path('newsdetails/<int:pk>/', views.newsdetails, name='newsdetails'),
    path('editnews/<int:pk>/', views.editnews, name='editnews'),
    path('deletenews/<int:pk>/', views.deletenews, name='deletenews'),
    #path('detailsnews/<int:pk>/', views.detailsnews, name='detailsnews'),
   
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    path('achievement/', views.achievement, name='achievement'),
    path('sports/', views.sports, name='sports'),
    path('event/', views.event, name='event'),
    path('cdc/', views.cdc, name='cdc'),
    path('ece/', views.ece, name='ece'),
    path('cse/', views.cse, name='cse'),
    path('ee/', views.ee, name='ee'),
    path('ce/', views.ce, name='ce'),
    path('me/', views.me, name='me'),
    path('annualfest/', views.annualfest, name='annualfest'),
    path('blood/', views.blood, name='blood'),
    path('dkb/', views.dkb, name='dkb'),
    path('guest/', views.guest, name='guest'),
    
    path('leader/', views.leader, name='leader'),
    path('times/', views.times, name='times'),
    path('tree/', views.tree, name='tree'),
    
    path('addnews/', views.addnews, name='addnews'),
    path('allnews/', views.allnews, name='allnews'),
    

]
