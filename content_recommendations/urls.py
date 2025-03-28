from django.urls import path
from .views import MakeRecommendationsAPIView

urlpatterns = [
    path(
        'recommendations/',
        MakeRecommendationsAPIView.as_view(),
        name='recommendations'
    ),
]
