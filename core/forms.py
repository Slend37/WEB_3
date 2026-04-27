from django import forms


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