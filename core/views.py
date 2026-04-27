from django.shortcuts import get_object_or_404, render
from core.models import Book


def index(request):
    context = {
        'title': 'Сервис обмена книгами',
        'welcome_text': 'Удобный и простой сайт для обмена книгами онлайн.',
        'books': Book.objects.order_by("-name").all(),
    }
    return render(request, 'core/index.html', context)

def about(request):
    return render(request, 'core/about.html')

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book,
    }
    return render(request, 'core/book_detail.html', context)