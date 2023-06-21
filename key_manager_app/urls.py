from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('access_keys/', views.access_keys, name='access_keys'),
    path('revoke_key/<int:key_id>/', views.revoke_key, name='revoke_key'),
    path('endpoint/', views.endpoint, name='endpoint'),
]
