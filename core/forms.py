from django import forms
from core.models import Book


class FeedbackForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        label="Тема письма",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите тему сообщения'
        })
    )
    email = forms.EmailField(
        label="Email отправителя",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    text = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите ваше сообщение здесь...'
        })
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'publish_year', 'author']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название книги'
            }),
            'publish_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 2024'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Название книги',
            'publish_year': 'Год издания',
            'author': 'Автор'
        }