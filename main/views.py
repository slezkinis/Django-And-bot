from django.shortcuts import render, HttpResponse
from .models import User


def index(request):
    users = User.objects.all().order_by('-score')
    about_users = []
    for num, user in enumerate(users, 1):
        about_users.append({'number': num, 'name': user.name, 'score': user.score})
    return render(request, 'index.html', context={'users': about_users})