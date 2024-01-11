from django.contrib import admin
from rest_framework import routers
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from bmstu_lab import auth_session

from bmstu_lab import views

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', views.filter, name='main'),
    path('<int:id>', views.get_first_aid, name='first_aid_url'),
    path('delete/', views.delete_first_aid, name='delete_first_aid'),  # Удаление мед. помощи
    #
    # API first_aid
    path(r'first_aid/', views.First_aid_List.as_view(), name='First_aid_List'),  # Список всех мед. помощей
    path(r'first_aid/<int:pk>/', views.get_first_aid_detail, name='First_aid_Detail'),  # Одна мед. помощи
    path(r'first_aid/<int:pk>/put/', views.update_first_aid, name='First_aid_Detail-put'),  # Обновление мед. помощи
    path(r'first_aid/create/', views.create_first_aid),  # Создание мед. помощи POST
    path(r'first_aid/delete/<int:id>', views.delete_first_aid_api),  # Удаление мед. помощи
    path(r'first_aid/add_to_trauma/<int:id>', views.add_first_aid_to_trauma),  # Добавление услуги в заявку

    # API trauma
    # path(r'trauma/create/', views.create_trauma),  # Создание поражения
    path(r'trauma/', views.get_trauma_all, name='trauma-list'),  # Просмотр всех поражений
    path(r'trauma/<int:id>/status_to_formed/', views.put_trauma_user),  # Обновление юзером
    path(r'trauma/<int:id>/status_to_end/', views.put_trauma_moderator),  # Смена статуса модератором
    path(r'trauma/<int:id>', views.get_trauma),  # Просмотр одного поражения
    path(r'trauma/<int:id>/delete', views.delete_trauma),  # Удаление введенной заявки
    path(r'trauma/first_aid/<int:id>/delete', views.delete_first_aid_from_trauma, name='delete_first_aid_from_trauma'),
    path(r'trauma/update_async/', views.put_async),
    # path(r'trauma/<int:id>/put', views.put_first_aid_in_trauma),  # Обновление полей повреждений
    # path(r'trauma/filter/', views.filter_trauma, name='filter_trauma'),
    #
    # # API first_aid_trauma
    # path(r'trauma_first_aid_list/', views.first_aid_list),  # получение списка м-м
    path(r'trauma/<int:id>/delete_first_aid/<int:id2>', views.del_trauma),  # удаление мед. помощи из заявки-поражения
    path(r'first_aid_trauma/<int:id>/<int:id2>/put', views.put_first_aid_trauma),

    path(r'auth/register/', auth_session.register, name='register'),
    path(r'auth/login/', auth_session.login, name='login'),
    path(r'auth/', auth_session.user, name='logout'),
    path(r'auth/logout/', auth_session.logout, name='logout'),

]
