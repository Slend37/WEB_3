from django.shortcuts import render

def index(request):
    context = {
        'title': 'Сервис обмена книгами',
        'welcome_text': 'Удобный и простой сайт для обмена книгами онлайн.'
    }
    return render(request, 'core/index.html', context)

def about(request):
    return render(request, 'core/about.html')