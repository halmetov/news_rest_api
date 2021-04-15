from django.shortcuts import render
from django.http import JsonResponse
from main.models import News


# Create your views here.


def indexHandler(request):
    print('request GET')
    print(request.GET)
    print('request POST')
    print(request.POST)
    news = News.objects.all()
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
                  "thumbnail": "https://media.guim.co.uk/d64524ce52e8e49c4fed52e385186842f7371ef2/0_486_5690_3416/500.jpg"
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
        new_n['webUrl'] = 'test'
        new_n['webPublicationDate'] = n.date
        #new_n['logo'] = n.logo
        
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

