from django.shortcuts import render, redirect
from .forms import WordForm

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