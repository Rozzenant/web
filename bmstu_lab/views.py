from django.shortcuts import render
from django.template.defaultfilters import linebreaksbr
import psycopg2

from pprint import pprint
import json

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from bmstu_lab.serializers import *
from bmstu_lab.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema


# if (Trauma.objects.filter(Status='Draft').count() == 0):
#     Trauma.create_draft_trauma()

def get_first_aid(request, id):
    first_aids_with_images = First_aid.objects.filter(First_aid_ID=id).exclude(Image_URL__exact='')
    if first_aids_with_images.exists():
        url =  first_aids_with_images[0].Image_URL.url
    else:
        url = None

    data = first_aids_with_images.filter(First_aid_ID=id).values()[0]
    data['Description'] = linebreaksbr(data['Description']) # отступы
    data['Image_URL'] = url

    return render(request, 'first_aid.html', data)

def filter(request):
    if (request.GET.get('reset') is not None):
        resetStatus()
    data = (First_aid.objects
            .filter(Status='1')
            .order_by('First_aid_ID'))
    search = ''
    if (request.GET.get('filter') is not None):
        search = request.GET.get('filter')
        data = data.filter(First_aid_Name__icontains=search)
    print(data, search)

    return render(request, 'main.html', {'data': data, 'search': search})



def change_status(id):
    conn = psycopg2.connect(dbname="medicine", host="localhost", user="postgres", password="adminros", port="5432")
    cursor = conn.cursor()

    cursor.execute(f"""UPDATE public.bmstu_lab_First_aid
                      set "Status"='0' 
                      where "First_aid_ID"={id}""")

    conn.commit()
    cursor.close()
    conn.close()

def resetStatus():
    conn = psycopg2.connect(dbname="medicine", host="localhost", user="postgres", password="adminros", port="5432")
    cursor = conn.cursor()
    cursor.execute('''UPDATE public.bmstu_lab_First_aid
                          SET "Status"='1' 
                          WHERE "First_aid_ID" IN 
                          (SELECT DISTINCT "First_aid_ID" FROM 
                          public.bmstu_lab_First_aid)''')
    conn.commit()
    cursor.close()
    conn.close()

def delete_first_aid(request):
    if request.method == 'POST':
        del_id = request.POST.get('delete')
        print(del_id)
        change_status(del_id)

    data = First_aid.objects.order_by('First_aid_ID').filter(Status='1')
    return render(request, 'delete.html', {'data': data})


class First_aid_List(APIView):
    model_class = First_aid
    serializer_class = First_aid_Serializer

    def get(self, request, format=None):
        """
        Возвращает список первых помощей
        """
        filter_search = request.GET.get('search')
        filter_from = request.GET.get('from')
        filter_to = request.GET.get('to')

        first_aid = self.model_class.objects.all()
        first_aid = first_aid.filter(Status='1')

        if filter_search:
            first_aid = first_aid.filter(First_aid_Name__icontains=filter_search)

        if filter_from:
            first_aid = first_aid.filter(Price__gte=filter_from)

        if filter_to:
            first_aid = first_aid.filter(Price__lte=filter_to)


        serializer = self.serializer_class(first_aid.order_by('First_aid_ID'), many=True)

        if Trauma.objects.filter(Status='Draft').exists():
            return Response(
                {'trauma_draft': Trauma.objects.get(Status='Draft').Trauma_ID,
                 'first_aids': serializer.data}
            )
        else:
            return Response(
                {'trauma_draft': None,
                 'first_aids': serializer.data}
            )

    @swagger_auto_schema(request_body=First_aid_Serializer)
    def post(self, request, format=None):
        """
        Добавляет новую процедуру
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class First_aid_Detail(APIView):
    model_class = First_aid
    serializer_class = First_aid_Serializer

    def get(self, request, pk, format=None):
        """
        Возвращает информацию о мед. процедуре
        """
        try:
            first_aid = First_aid.objects.get(First_aid_ID=pk,
                                              Status='1')
        except First_aid.DoesNotExist:
            return Response({'detail': 'Не найдена услуга'}, status=status.HTTP_404_NOT_FOUND)

        first_aid = first_aid
        serializer = self.serializer_class(first_aid)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Создает услугу
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=First_aid_Serializer)
    def put(self, request, pk, format=None):
        """
        Обновляет информацию о мед. процедуре (для модератора)
        """
        first_aid = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(first_aid, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=First_aid_Serializer)
@api_view(['put'])
def add_first_aid_to_trauma(request, id, format=None):
    try:
        first_aid = First_aid.objects.get(First_aid_ID=id)
    except First_aid.DoesNotExist:
        return Response({'detail': 'Такой услуги не существует'},status=status.HTTP_404_NOT_FOUND)

    trauma_draft = Trauma.get_draft_trauma()
    if first_aid not in trauma_draft.First_aid_in_Trauma_List.all():
        trauma_draft.First_aid_in_Trauma_List.add(first_aid)
        return Response({'detail': 'Услуга успешно добавлена в заявку'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Услуга уже присутствует в заявке'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['delete'])
def delete_first_aid_api(request, id, format=None):
    """
    Удаление первой помощи
    """
    try:
        first_aid = First_aid.objects.get(First_aid_ID=id)
    except First_aid.DoesNotExist:
        return Response({'detail': 'Услуга не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if first_aid and (first_aid.Status != '0'):
        first_aid.Status = '0'
        first_aid.save()
        return Response({'detail': 'Услуга удалена'},status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'detail': 'Услуга не найдена'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['get'])
def get_trauma_all(request, format=None):
    """
    Возвращает список поражений (заявок)
    """
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    status_filter = request.GET.get('Status')

    data = Trauma.objects.order_by('Status', 'Date_Creation')
    data = data.exclude(Status__in=['Deleted', 'Draft'])
    show_time = True

    if date_from:
        data = data.filter(Date_Approving__gte=date_from)
        show_time = False
    if date_to:
        data = data.filter(Date_Approving__lte=date_to)
        show_time = False
    if status_filter:
        data = data.filter(Status=status_filter)
        show_time = False
    def custom_sort(item):

        status_order = {"Formed": 1, 'Completed': 2, 'Cancelled': 3}.get(item.Status, 4)
        return (item.Date_Creation, status_order)

    sorted_data = sorted(data, key=custom_sort)
    serializer = Trauma_Serializer(sorted_data, many=True, context={'show_time': show_time})
    if not serializer.data:
        return Response({'detail': 'Заявок не найдено'},status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['post'])
def create_trauma(request, format=None):
    """
    Добавляет новое повреждение
    """
    serializer = Trauma_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])
def put_trauma_user(request, id, format=None):
    """
    Создатель формирует меняет статус заявки с черновика в сформированную
    """
    User_ID = singleton()
    if Trauma.objects.filter(Status="Draft").exists():
        trauma = Trauma.get_draft_trauma()
        if (trauma.Creator == User_ID) and (trauma.Trauma_ID == id):
            if trauma.First_aid_in_Trauma_List.count() == 0:
                return Response({'detail': 'Нельзя сформировать пустую заявку'},
                            status=status.HTTP_400_BAD_REQUEST)
            trauma.Status = 'Formed'
            trauma.Date_Approving = timezone.now()
            trauma.save()
            return Response({'detail': f'Статус заявки id: {trauma.Trauma_ID} успешно изменен.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Нельзя менять не свою заявку'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Черновая заявка не создана"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['Put'])
def put_trauma_moderator(request, id, format=None):
    """
    Модератор меняет статус
    """
    try:
        trauma = Trauma.objects.get(Trauma_ID=id)
    except Trauma.DoesNotExist:
        return Response({'detail': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)


    if trauma.Status == 'Formed':
        status_request = request.data.get('Status')
        if status_request in ['Completed', 'Cancelled']:
            trauma.Status = status_request
            trauma.Date_End = timezone.now()
            trauma.Moderator = Users.objects.get(User_ID=2)
            trauma.save()
            return Response({'detail': f'Статус заявки id: {trauma.Trauma_ID} изменен на {trauma.Status}'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Неверный статус, должен быть in ["Completed", "Cancelled"]'})
    else:
        return Response({'detail': 'Неподходящий статус изменяемой заявки, должен быть Formed'},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get'])
def get_trauma(request, id, format=None):
        """
        Возвращает одну медицинскую категорию (заявку)
        """
        try:
            trauma = Trauma.objects.get(Trauma_ID=id)
        except Trauma.DoesNotExist:
            return Response({'detail': 'Заявки с таким id не существует'},status=status.HTTP_404_NOT_FOUND)

        if trauma.Status not in ['Deleted']:
            serializer = Trauma_Serializer(trauma)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Заявки с таким id не существует'},status=status.HTTP_404_NOT_FOUND)
#
#
@api_view(['Delete'])
def del_trauma(request, id, id2, format=None):
    """
    Удаляет первую помощь из поражений
    """
    trauma_firts_aid = get_object_or_404(First_aid_Trauma, Trauma_ID=id, First_aid_ID=id2)
    trauma_firts_aid.delete()

    return Response({'detail': f'Удалено {id} - {id2} id заявки и услуги'},status=status.HTTP_204_NO_CONTENT)


@api_view(['Delete'])
def delete_first_aid_from_trauma(request, id, format=None):
    """
    Удаление услуги из заявки
    """
    trauma = Trauma.get_draft_trauma()
    try:
        first_aid = First_aid.objects.get(First_aid_ID=id)
    except First_aid.DoesNotExist:
        return Response({'detail': 'Такой услуги не существует'},status=status.HTTP_404_NOT_FOUND)

    if first_aid.Status == '1':
        if first_aid in trauma.First_aid_in_Trauma_List.all():
            trauma.First_aid_in_Trauma_List.remove(first_aid)
            return Response({'detail': 'Услуга успешно удалена из заявки'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Услуга не найдена в заявке'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Такой услуги не существует'},status=status.HTTP_404_NOT_FOUND)


@api_view(['delete'])
def delete_trauma(request, id, format=None):
    try:
        trauma = Trauma.objects.get(Trauma_ID=id)
    except Trauma.DoesNotExist:
        return Response({'detail': 'Такой заявки не существует'},status=status.HTTP_404_NOT_FOUND)

    if trauma.Status == 'Deleted':
        return Response({'detail': 'Такой заявки не существует'},status=status.HTTP_404_NOT_FOUND)

    if trauma.Creator != singleton():
        return Response({'detail': 'У вас нет прав для удаления этой заявки'}, status=status.HTTP_400_BAD_REQUEST)

    trauma.Status = 'Deleted'
    trauma.save()
    return Response({'detail': 'Заявка успешно удалена'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['put'])
def put_first_aid_in_trauma(request, id, format=None):
    trauma = get_object_or_404(Trauma, pk=id)
    serializer = Trauma_Serializer(trauma, data=request.data, partial=True)

    first_aid_list = request.data.get('First_aid_in_Trauma_List', [])
    first_aid_error = []
    if type(first_aid_list) != list:
        first_aid_list = [first_aid_list]
    for i in first_aid_list:
        if not First_aid.objects.filter(First_aid_ID=i).exists():
            first_aid_error.append(i)
    if first_aid_error:
        return Response({'details': f'Нет в БД: {first_aid_error}'}, status=status.HTTP_400_BAD_REQUEST)

    trauma.First_aid_in_Trauma_List.clear()
    for i in first_aid_list:
        if not First_aid_Trauma.objects.filter(Trauma_ID=trauma, First_aid_ID=i).exists():
            First_aid_Trauma.objects.create(Trauma_ID=trauma, First_aid_ID_id=i)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['put'])
def put_first_aid_trauma(request, id, id2, format=None):
    data = {'First_aid_ID': id2, 'Trauma_ID': id}
    serializer = First_aid_Trauma_Serializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        data["First_aid_ID"] = serializer.data.get("First_aid_ID")
        data["Trauma_ID"] = serializer.data.get("Trauma_ID")
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def put_async(request, format=None):
    """
    Обновляет данные травмы асинхронно
    """
    expected_token = '7a4f891b2e613dca'

    if request.method != 'PUT':
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    trauma_id = request.data.get('id')
    result = request.data.get('result')
    token = request.data.get('token')

    if token != expected_token:
        return Response({'error': 'Недопустимый токен'}, status=status.HTTP_403_FORBIDDEN)

    if not trauma_id or not result :
        return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        trauma = Trauma.objects.get(Trauma_ID=trauma_id)
    except Trauma.DoesNotExist:
        return Response({'error': 'Травма не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if trauma.Confirmation_Doctor in ['Confirmed', 'Rejected']:
        return Response({'details': 'Врач уже словесно подтвердил или отклонил заявку'}, status=status.HTTP_403_FORBIDDEN)

    if 'Confirmed' in result:
        trauma.Confirmation_Doctor = 'Confirmed'
    elif 'Rejected' in result:
        trauma.Confirmation_Doctor = 'Rejected'

    trauma.save()
    serializer = Trauma_Serializer(trauma, context={'show_traumas': False})
    return Response(serializer.data)



