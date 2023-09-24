from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# from django.shortcuts import redirect

from datetime import date

# Create your views here.
# def hello(request):
#     return HttpResponse("Hello world!")

def hello(request):
    return render(request, 'index.html', {
        'data': {
            'current_date': date.today(),
            'list': ['Python', 'BMSTU', 'Django']
        }
    })
# def GetOrders(request):
#     return render(request, 'orders.html', data)

def GetOrder(request, id):
    fast_data = data['data']['orders'][id - 1]
    return render(request, 'order.html', {
        'data':{
            'current_date': date.today(),
            'id': id,
            'title': fast_data['title'],
            'link': fast_data['link'],
            'description': fast_data['description']
        }
    })

def sendText(request):
    return render(request, 'send-text.html')

def sendTextPOST(request):
    text = request.POST['text']
    return render(request, 'sendTextPost.html', {
        'response': text
    })

def filter(request):
    if (request.GET.get('filter') is not None):
        search = request.GET.get('filter').lower()
    else:
        return render(request, 'filter.html', data)

    fast_data = data['data']['orders']
    data_filter = {'data':{'orders':[]}}
    data_filter['data'].setdefault('value', search)

    for data_search in fast_data:
        if (search in data_search['title'].lower() or search in data_search['description']):
            data_filter['data']['orders'].append(
                {'id': data_search['id'],
                 'title': data_search['title'],
                 'description': data_search['description'],
                 'link': data_search['link']}
            )


    return render(request, 'filter.html', data_filter)

data = {
        'data':{
            'orders': [
        {'id': 1, 'title': 'Первая помощь при термических ожогах', 'link':
            'https://ss.sport-express.ru/userfiles/materials/178/1787924/large.jpg', 'description': 'Что делать если '
                                                                                                    'Вы случайно '
                                                                                                    'пролили чайник '
                                                                                                    'на себя?'},
        {'id': 2, 'title': 'Первая помощь при химических ожогах', 'link':
            'https://polyclin.ru/upload/medialibrary/6fa/6faeaf331436779915adae22884a72a8.jpg', 'description': 'Как '
                                                                                                               'избавиться '
                                                                                                               'от последствий '
                                                                                                               'химического '
                                                                                                               'ожога?'},
        {'id': 3, 'title': 'Первая помощь при солнечном ожоге',
         'link': 'https://polyclinika.ru/upload/medialibrary/920/kxfxzr16o9pgsza25huhr9jn8pv7j34k/Ozhogi.jpg',
         'description': 'Что делать, если Вы перележали на солнце?'},
        {'id': 4, 'title': 'Первая помощь при облучении', 'link':
            'https://ae04.alicdn.com/kf/U9ae510b501d0450abd139a7373870ef1X.png', 'description': 'Как спастись от '
                                                                                                'радиации в домашних '
                                                                                                'условиях?'},
        {'id': 5, 'title': 'Первая помощь при ЧМТ',
         'link': 'https://armedical.co.il/wp-content/uploads/2018/07/Reabilitatsiya-posle-cherepno-mozgovoj-travmy-700x458.jpg',
         'description': 'Удар тупым предметом или что делать с сотрясением мозга?'},
        {'id': 6, 'title': 'Первая помощь при переломах',
         'link': 'https://www.smclinic.ru/upload/iblock/c4d/771j9kspgqdn4rmgcbgf9o31wpt8kcmd.jpg',
         'description': 'Открытый перелом и как его лечить'}
            ]
        }
}