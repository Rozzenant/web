from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from bmstu_lab import views

router = routers.DefaultRouter()

urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', views.filter, name='main'),
    path('<int:id>', views.GetProcedure, name='order_url'),
    path('delete/', views.deleteProcedure, name='delete_procedure'),  # Удаление процедуры

    # API medical-procedures
    path(r'medical-procedures/', views.MP_List.as_view(), name='MP-list'),  # Список всех процедур
    path(r'medical-procedures/<int:pk>/', views.MP_Detail.as_view(), name='MP-detail'),  # Одна процедура
    path(r'medical-procedures/<int:pk>/put/', views.MP_Detail.as_view(), name='MP-put'),  # Обновление процедуры
    path(r'medical-procedures/create/', views.create_MedProc),  # Создание процедуры
    # path(r'medical-procedures/delete/<int:id>', views.delete_MedProc),  # Удаление процедуры

    # API medical-categories
    path(r'medical-categories/create/', views.create_MedCat),  # Создание категории
    path(r'medical-categories/', views.get_MedCats, name='MC-list'),  # Просмотр всех категорий
    path(r'medical-categories/<int:id>/update_user/', views.put_MedCat_user),  # Обновление юзером
    path(r'medical-categories/<int:id>/update_moderator/', views.put_MedCat_moderator),  # обновление модератором
    path(r'medical-categories/<int:id>', views.get_MedCat),  # Просмотр одной категории
    path(r'medical-categories/<int:id>/delete', views.deleteCategory, name='delete_category'),  # удаление заявки
    path(r'medical-categories/<int:id>/delete_MedCat/<int:id2>', views.del_MedCat),  # удаление процедуры из категории
    path(r'medical-categories/filter/', views.mcFilter, name='mcFilter'),

    # API ProcCat
    path(r'proccat/', views.get_ProcCat),  # получение списка м-м

]
