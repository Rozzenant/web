from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path
from bmstu_lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.filter, name='filter'),
    path('<int:id>', views.GetOrder, name='order_url'),

    # path('hello/', views.hello),
    # path('', views.GetOrders, name='main-page'),
    # path('sendText/', views.sendText, name='sendText'),
    # path('sendText/sendTextPOST', views.sendTextPOST),
]
