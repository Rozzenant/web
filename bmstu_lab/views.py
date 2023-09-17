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
    return render(request, 'orders.html', {
        'data':{
            'current_date': date.today(),
            'orders':[
                {'title': 'Книга с картинками', 'id': 1},
                {'title': 'Тарелка', 'id': 2},
                {'title': 'Кот', 'id': 3}
            ]
        }
    })

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