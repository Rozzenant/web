from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path
from bmstu_lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('<int:id>', views.GetProcedure, name='order_url'),
    path('delete/', views.deleteProcedure, name='delete_procedure')

    # path('hello/', views.hello),
    # path('', views.GetOrders, name='main-page'),
    # path('sendText/', views.sendText, name='sendText'),
    # path('sendText/sendTextPOST', views.sendTextPOST),
]
