from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.start, name='start'),
    path('next', views.next, name='next'),
    path('predict', views.predict, name='predict'),
    path('next_predict', views.next_predict, name='next_predict'),
]
