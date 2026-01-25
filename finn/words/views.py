from django.shortcuts import render

# Create your views here.

def user_words(req):
    if req.user.is_authenticated:
        words = req.user.word.all()
        return render(req, 'home.html', {'words': words})
    else:
        return render(req, 'home.html', {'words': []})