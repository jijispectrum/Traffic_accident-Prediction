from django.urls import path
from . import views
from .views import predict_view
urlpatterns = [
    path('', predict_view, name='predict'),
    # path('map/', views.map_view, name='map_view'), # Route for accident prediction
]
