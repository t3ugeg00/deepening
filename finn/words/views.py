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

def random_word(req):
    if not req.user.is_authenticated:
        return render(req, 'card.html', {'word': {}})
    
    count = req.user.word.count()

    if count == 0:
        word = {}
    else:
        i = random.randint(0, count - 1)
        word = Word.objects.all()[i]

    return render(req, 'card.html', {'word': word})