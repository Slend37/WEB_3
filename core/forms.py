from django import forms
from core.models import Book, Author


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
        fields = ['name', 'publish_year']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название книги'
            }),
            'publish_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 2024',
                'min': 0,
                'max': 2030
            })
        }
        labels = {
            'name': 'Название книги',
            'publish_year': 'Год издания',
        }
    
    def clean_publish_year(self):
        year = self.cleaned_data.get('publish_year')
        from django.utils import timezone
        current_year = timezone.now().year
        if year < 0 or year > current_year + 5:
            raise forms.ValidationError(f'Год издания должен быть между 0 и {current_year + 5}')
        return year
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Название книги должно содержать минимум 2 символа')
        return name