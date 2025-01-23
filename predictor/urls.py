from django.urls import path
from . import views

urlpatterns = [
    path('traffic-hotspots/', views.predict_hotspot, name='predict_hotspot'),
]
