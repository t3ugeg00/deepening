from django.urls import path, include
from .views import user_words, delete_word, random_word

urlpatterns = [
    path('', user_words, name='home'),
    path('word/delete/<int:pk>', delete_word, name='delete_word'),
    path('card', random_word, name='card')
]