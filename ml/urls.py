from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/translate/', views.translate, name='translate'),
    path('api/gestures/', views.gestures, name='synced_gestures'),
    path('api/sync/', views.sync, name='sync'),
    path('api/removeSyncedGesture/', views.remove_synced_gesture, name='remove'),
    path('api/reset/', views.reset, name='reset'),
]