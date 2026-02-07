from django.shortcuts import render, redirect, get_object_or_404
from .forms import WordForm
from .models import Word
import random

# Create your views here.

def user_words(req):
    if req.user.is_authenticated:
        if req.method == "POST":
            form = WordForm(req.POST)
            if form.is_valid():
                word = form.save(commit=False)
                word.user = req.user
                word.save()
                return redirect('home')
        else:
            form = WordForm()
        words = req.user.word.all()
        return render(req, 'home.html', {'words': words, 'form': form})
    else:
        return render(req, 'home.html', {'words': []})
    
def delete_word(req, pk):
    word = get_object_or_404(Word, pk=pk, user=req.user)

    if req.method == 'POST':
        word.delete()

    return redirect('home')

def shuffled_words(req):
    if not req.user.is_authenticated:
        return render(req, 'card.html', {'words': []})
    
    words = req.user.word.order_by("?").values("eng", "fin")

    return render(req, 'card.html', {'words': list(words)})