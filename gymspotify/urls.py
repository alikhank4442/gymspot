from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated, GetRecomendation

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('get-recomendation', GetRecomendation.as_view())
    
    
]