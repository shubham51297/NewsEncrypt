from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('login/', views.index, name='index'),
    path('addUser/', views.addSource),
    path('addMessage/<str:username>', views.addMessage),
    path('allMessage/<str:currenteditor>', views.allMessage),
    path('singleMessage/<int:id>',views.singleMessage),
    path('addSource/<str:username>',views.addSource),
    path('editor/<str:username>',views.editor),
    path('checkSQL/',views.checkSQL)

]