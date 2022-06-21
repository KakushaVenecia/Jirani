from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns=[
    path('',views.index, name = 'home'),
    path('userlogin/',views.signin, name='userlogin'), 
    path('register/',views.register, name='register'), 
    path('logout/',views.signout, name='logout'),

    path('new-hood/', views.new_hood, name='new-hood'),
    path('hoods/', views.hoods, name='hoods'),
    path('join_hood/<id>', views.join_hood, name='join-hood'),

    path('one_hood/<hood_id>', views.one_hood, name='one-hood'),
    path('leave_hood/<id>', views.leave_hood, name='leave-hood'), 
    path('addbusiness/<hood_id>', views.add_business, name='add-business'),
    path('<hood_id>/new-post', views.new_post, name='post'),

    
    path('myprofile/', views.myprofile, name='myprofile'),
    path('myprofile/<username>/edit/', views.edit_profile, name='updateprofile'),
    
    path('search/', views.search_business, name='search'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)