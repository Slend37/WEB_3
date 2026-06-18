from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from core.models import Book, Author, Comment
from core.forms import CommentForm, FeedbackForm, BookForm


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/about.html')


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


class BookListView(ListView):
    model = Book
    template_name = 'core/index.html'
    context_object_name = 'books'
    ordering = ['-name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сервис обмена книгами'
        context['welcome_text'] = 'Удобный и простой сайт для обмена книгами онлайн.'
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'core/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'core/book_form.html'
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        author_name = self.request.user.username
        author, created = Author.objects.get_or_create(name=author_name)
        form.instance.author = author
        
        messages.success(self.request, f'Книга "{form.instance.name}" успешно создана!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление новой книги'
        context['button_text'] = 'Создать книгу'
        context['action'] = 'create'
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'core/book_form.html'
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Книга "{form.instance.name}" успешно обновлена!')
        return super().form_valid(form)
    
    def test_func(self):
        book = self.get_object()
        return self.request.user == book.owner
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование книги: {self.object.name}'
        context['button_text'] = 'Сохранить изменения'
        context['action'] = 'edit'
        return context


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'core/book_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        book = self.get_object()
        return self.request.user == book.owner
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Книга успешно удалена!')
        return super().delete(request, *args, **kwargs)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            Comment.objects.create(
                book=book,
                author=request.user,
                text=form.cleaned_data["text"],
            )
            messages.success(request, "Комментарий успешно добавлен")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
        
        return HttpResponseRedirect(reverse_lazy('book_detail', kwargs={'pk': book_id}))