from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from core.models import Book
from core.forms import FeedbackForm


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

def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print("=" * 50)
            print("Новое сообщение из формы обратной связи:")
            print(f"Тема: {form.cleaned_data['subject']}")
            print(f"Email: {form.cleaned_data['email']}")
            print(f"Сообщение: {form.cleaned_data['text']}")
            print("=" * 50)
            return redirect('home')
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
        'title': 'Контакты',
    }
    return render(request, 'core/contact.html', context)