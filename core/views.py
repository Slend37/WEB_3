from django.shortcuts import get_object_or_404, render
from core.models import Book
from django.http import HttpRequest, HttpResponse


def index(request):
    context = {
        'title': 'Сервис обмена книгами',
        'welcome_text': 'Удобный и простой сайт для обмена книгами онлайн.',
        'books': Book.objects.order_by("-name").all(),
    }
    return render(request, 'core/index.html', context)

def about(request):
    return render(request, 'core/about.html')