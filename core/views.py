from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from core.models import Book, Author, Comment
from core.forms import CommentForm, FeedbackForm, BookForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Сервис обмена книгами',
        'welcome_text': 'Удобный и простой сайт для обмена книгами онлайн.',
        'books': Book.objects.order_by("-name").all(),
    }
    return render(request, 'core/index.html', context)

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/about.html')

def book_detail(request: HttpRequest, pk) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book,
        'form': CommentForm(),
    }
    return render(request, 'core/book_detail.html', context)

def add_comment(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                book = book,
                author=request.user,
                text=form.cleaned_data["text"],
            )
            messages.success(request, "Комментарий успешно добавлен")
            return redirect(reverse("book_detail", args=[book_id]))
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
            return redirect(reverse("book_detail", args=[book_id]))
    else:
        return HttpResponse("Метод не поддерживается", status=405)



def contact(request: HttpRequest) -> HttpResponse:
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

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            
            author_name = request.user.username
            author, created = Author.objects.get_or_create(name=author_name)
            book.author = author
            
            book.save()
            messages.success(request, f'Книга "{book.name}" успешно создана!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'title': 'Добавление новой книги',
        'button_text': 'Создать книгу',
        'action': 'create'
    }
    return render(request, 'core/book_form.html', context)

@login_required
def book_edit(request: HttpRequest, pk) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    
    if book.user != request.user:
        messages.error(request, 'Вы можете редактировать только свои книги!')
        return redirect('book_detail', pk=book.pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.name}" успешно обновлена!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'title': f'Редактирование книги: {book.name}',
        'button_text': 'Сохранить изменения',
        'action': 'edit'
    }
    return render(request, 'core/book_form.html', context)

def register(request: HttpRequest) -> HttpResponse:
    error = "Пожалуйста, исправьте ошибки в форме"
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        else:
            return render(request, "registration/register.html", {"form": form, "error": error})
    else:
        form = UserCreationForm()
        return render(request, "registration/register.html", {"form": form})