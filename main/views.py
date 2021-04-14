from django.shortcuts import render
from django.http import JsonResponse
from main.models import News


# Create your views here.


def indexHandler(request):
    news = News.objects.all()
    new_news = []
    for n in news:
        new_n = {}
        new_n['title'] = n.title
        new_n['category'] = n.category.title
        new_n['description'] = n.description
        new_n['author'] = n.author
        new_n['date'] = n.date
        #new_n['logo'] = n.logo
        new_n['status'] = n.status
        new_n['rating'] = n.rating

        new_news.append(new_n)

    return JsonResponse({'success': True, '_success': True, 'news': new_news})