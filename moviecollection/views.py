from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    context = {
        'message': 'You found it!'
    }
    return render(request, 'moviecollection/index.html', context=context)
