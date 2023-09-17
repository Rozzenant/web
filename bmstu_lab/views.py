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
def GetOrders(request):
    return render(request, 'orders.html', data)

def GetOrder(request, id):
    return render(request, 'order.html', {
        'data':{
            'current_date': date.today(),
            'id': id
        }
    })

def sendText(request):
    return render(request, 'send-text.html')

def sendTextPOST(request):
    text = request.POST['text']
    return render(request, 'sendTextPost.html', {
        'response': text
    })

data = {
        'data':{
            'current_date': date.today(),
            'orders': [
        {'id': 1, 'title': 'Первая помощь при термических ожогах', 'link':
            'https://ss.sport-express.ru/userfiles/materials/178/1787924/large.jpg'},
        {'id': 2, 'title': 'Первая помощь при химических ожогах', 'link': 'https://polyclin.ru/upload/medialibrary/6fa/6faeaf331436779915adae22884a72a8.jpg'},
        {'id': 3, 'title': 'первая помощь по чему-то',
         'link': 'https://polyclinika.ru/upload/medialibrary/920/kxfxzr16o9pgsza25huhr9jn8pv7j34k/Ozhogi.jpg'},
        {'id': 4, 'title': 'Радиация', 'link': 'https://ae04.alicdn.com/kf/U9ae510b501d0450abd139a7373870ef1X.png'},
        {'id': 5, 'title': 'Мелас'},
        {'id': 6, 'title': 'Мелас'}
            ]
        }
}