from django.urls import path, include
from .views import user_words

urlpatterns = [
    path('', user_words, name='home')
]