from django.shortcuts import render
from django.http import JsonResponse
from main.models import News
from datetime import datetime


# Create your views here.


def indexHandler(request):
    section = request.GET.get('section', '')
    page_size = int(request.GET.get('page-size', 10))
    orderby = request.GET.get('order-by', 'newest')
    from_date = request.GET.get('from-date', None) #2021-04-14

    if from_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')

    if section:
        if orderby == 'newest':
            if from_date:
                news = News.objects.filter(category__title=section).filter(date__gte=from_date).order_by('-date')[0:page_size]
            else:
                news = News.objects.filter(category__title=section).order_by('-date')[0:page_size]

        elif orderby == 'oldest':
            if from_date:
                news = News.objects.filter(category__title=section).filter(date__gte=from_date).order_by('date')[0:page_size]
            else:
                news = News.objects.filter(category__title=section).order_by('date')[0:page_size]

        elif orderby == 'relevance':
            if from_date:
                news = News.objects.filter(category__title=section).filter(status=0).filter(date__gte=from_date).order_by('-date')[0:page_size]
            else:
                news = News.objects.filter(category__title=section).filter(status=0).order_by('-date')[0:page_size]

        else:
            if from_date:
                news = News.objects.filter(category__title=section).filter(date__gte=from_date)[0:page_size]
            else:
                news = News.objects.filter(category__title=section)[0:page_size]
    else:
        if orderby == 'newest':
            if from_date:
                news = News.objects.all().filter(date__gte=from_date).order_by('-date')[0:page_size]
            else:
                news = News.objects.all().order_by('-date')[0:page_size]

        elif orderby == 'oldest':
            if from_date:
                news = News.objects.all().filter(date__gte=from_date).order_by('date')[0:page_size]
            else:
                news = News.objects.all().order_by('date')[0:page_size]

        elif orderby == 'relevance':
            if from_date:
                news = News.objects.filter(status=0).filter(date__gte=from_date).order_by('-date')[0:page_size]
            else:
                news = News.objects.filter(status=0).order_by('-date')[0:page_size]

        else:
            news = News.objects.all()[0:page_size]
    new_news = []
    for n in news:
        new_n = {
                "id": "",
                "type": "liveblog",
                "sectionId": "business",
                "sectionName": "",
                "webPublicationDate": "",
                "webTitle": "",
                "webUrl": "https://www.theguardian.com/business/live/2021/apr/15/deliveroo-hut-group-naked-wines-pandemic-sales-stock-markets-ftse-dow-bitcoin-business-live",
                "apiUrl": "https://content.guardianapis.com/business/live/2021/apr/15/deliveroo-hut-group-naked-wines-pandemic-sales-stock-markets-ftse-dow-bitcoin-business-live",
                "fields": {
                  "trailText": "",
                  "thumbnail": ""
                },
                "tags": [],
                "isHosted": False,
                "pillarId": "pillar/news",
                "pillarName": "News"
              }
        new_n['id'] = str(n.id)
        new_n['webTitle'] = n.title
        new_n['sectionName'] = n.category.title
        new_n['fields']['trailText'] = n.description
        new_n['fields']['thumbnail'] = request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/media/' + n.logo.name
        new_n['webUrl'] = request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/news/' + str(n.id)
        new_n['apiUrl'] = request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/api/' + str(n.id)
        new_n['webPublicationDate'] = n.date.strftime("%m/%d/%Y, %H:%M:%S")
        new_n['tags'] = [
            {

                "id": "",
                "type": "",
                "webTitle": n.author,
                "webUrl": request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/news/' + str(n.id),
                "apiUrl": request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/api/' + str(n.id),
                "references": [],
                "bio": n.author,
                "bylineImageUrl": request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/media/' + n.logo.name,
                "firstName": n.author,
                "lastName": ""
            }
        ]

        new_news.append(new_n)
    
    response = {
        "status": "ok",
        "userTier": "developer",
        "total": len(news),
        "startIndex": 1,
        "pageSize": 10,
        "currentPage": 1,
        "pages": 1,
        "orderBy": "newest",
        "results": new_news
    }
    return JsonResponse({'success': True, '_success': True, 'response':response})


def news_detailHandler(request ,news_id):
    new = News.objects.get(id=int(news_id))

    return render(request, 'news-id.html', {'new': new})


def newsHandler(request):
    news = News.objects.all().order_by('-category__news__date')

    return render(request, 'news.html', {'news': news})



def news_api_detailHandler(request ,news_id):
    new = News.objects.get(id=int(news_id))
    response = {
            "status": "ok",
            "userTier": "developer",
            "total": 1,
            "content": {
                "id": str(new.id),
                "type": "liveblog",
                "sectionId": "business",
                "sectionName": new.category.title,
                "webPublicationDate": new.date,
                "webTitle": new.title,
                "webUrl": request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/news/' + str(new.id),
                "apiUrl": request.META.get('wsgi.url_scheme', '') + '://' + request.META.get('HTTP_HOST', '') + '/api/' + str(new.id),
                "isHosted": False,
                "pillarId": "pillar/news",
                "pillarName": "News"
            }
        }


    return JsonResponse({'success': True, '_success': True, 'response':response})

