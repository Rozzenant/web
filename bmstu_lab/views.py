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
from bmstu_lab.serializers import MP_Serializer, MC_Serializer, CP_Serializer
from bmstu_lab.models import MedicalProcedures, MedicalCategories, CategoriesProcedures
from rest_framework.views import APIView
from rest_framework.decorators import api_view

def GetProcedure(request, id):
    medical_procedures_with_images = MedicalProcedures.objects.filter(Procedure_ID=id).exclude(Image_URL__exact='')
    url = medical_procedures_with_images[0].Image_URL.url

    data = {'data': MedicalProcedures.objects.filter(Procedure_ID=id).values()[0]}
    data['data']['Description'] = linebreaksbr(data['data']['Description']) # add indents to the text, as in the database
    data['data']['Image_URL'] = url

    return render(request, 'procedure.html', data)

def filter(request):
    if (request.GET.get('reset') is not None):
        resetStatus()

    data = {
        'data': MedicalProcedures.objects
        .order_by('Procedure_ID')
        .filter(Status='1')
    }
    for i in data['data']:
        print(i.Image_URL)


    if (request.GET.get('filter') is not None):
        search = request.GET.get('filter')

        data_filter = {
            'data': MedicalProcedures.objects
            .filter(Procedure_Name__icontains=search)
            .filter(Status='1')
            .order_by('Procedure_ID')
        }

        return render(request, 'main.html', data_filter)
    else:
        return render(request, 'main.html', data)



def change_status(id):
    conn = psycopg2.connect(dbname="medicine", host="localhost", user="postgres", password="adminros", port="5432")
    cursor = conn.cursor()

    cursor.execute('''UPDATE public.bmstu_lab_medicalprocedures 
                      set "Status"='0' 
                      where "Procedure_ID"=%s''',(id))

    conn.commit()
    cursor.close()
    conn.close()

def resetStatus():
    conn = psycopg2.connect(dbname="medicine", host="localhost", user="postgres", password="adminros", port="5432")
    cursor = conn.cursor()
    cursor.execute('''UPDATE public.bmstu_lab_medicalprocedures 
                          SET "Status"='1' 
                          WHERE "Procedure_ID" IN 
                          (SELECT DISTINCT "Procedure_ID" FROM 
                          public.bmstu_lab_medicalprocedures)''')
    conn.commit()
    cursor.close()
    conn.close()

def deleteProcedure(request):
    if request.method == 'POST':
        del_id = request.POST.get('delete')
        change_status(del_id)

    data = {'data': MedicalProcedures.objects.order_by('Procedure_ID').filter(Status='1')}
    return render(request, 'delete.html', data)


class MP_List(APIView):
    model_class = MedicalProcedures
    serializer_class = MP_Serializer

    def get(self, request, format=None):
        """
        Возвращает список медицинских процедур
        """
        filter_search = request.GET.get('filter_search')
        status = request.GET.get('status')

        MedicalProcedures = self.model_class.objects.all()

        if filter_search:
            MedicalProcedures = MedicalProcedures.filter(Procedure_Name__icontains=filter_search)
        if status:
            MedicalProcedures = MedicalProcedures.filter(Status=status)

        serializer = self.serializer_class(MedicalProcedures.order_by('Procedure_ID'), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Добавляет новую процедуру
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MP_Detail(APIView):
    model_class = MedicalProcedures
    serializer_class = MP_Serializer

    def get(self, request, pk, format=None):
        """
        Возвращает информацию о мед. процедуре
        """
        med_proc = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(med_proc)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Обновляет информацию о мед. процедуре (для модератора)
        """
        med_proc = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(med_proc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Удаляет информацию о мед. процедуре
        """
        med_proc = get_object_or_404(self.model_class, pk=pk)
        med_proc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_MedCats(request, format=None):
    """
    Возвращает список медицинских категорий (заявок)
    """
    date_filter = request.GET.get('date')
    status_filter = request.GET.get('status')

    data = MedicalCategories.objects.order_by('Status', 'Date_Creation')

    if date_filter:
        data = data.filter(Date_Creation=date_filter)
    if status_filter:
        data = data.filter(Status=status_filter)


    # Функция сравнения для кастомной логики сортировки
    def custom_sort(item):
        status_order = {"i": 0, "w": 1}.get(item.Status, 2)
        return (item.Date_Creation, -status_order) # "-" Для сортировки от "i" к "w"

    sorted_data = sorted(data, key=custom_sort, reverse=True)
    serializer = MC_Serializer(sorted_data, many=True)
    return Response(serializer.data)

@api_view(['Post'])
def create_MedProc(request, format=None):
    """
    Добавляет новую мед. процедуру
    """
    serializer = MP_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])
def put_MedCat_user(request, id, format=None):
    """
    Пользователь обновляет информацию о мед. категории (заявка)
    """
    User_ID = 1

    med_cat = get_object_or_404(MedicalCategories, pk=id)
    serializer = MC_Serializer(med_cat, data=request.data, partial=True)
    if serializer.is_valid():
        if med_cat.ID_Creator.User_ID != User_ID:
            return Response('У вас нет доступа к этой заявке')
        status = request.data.get("Status")
        print(status)
        status = status if status else med_cat.Status


        if status in ["i", "d"]:
            med_cat.Status = status
        else:
            return Response("Доступ запрещен")

        serializer.save()

        med_proc_list = request.data.get("MedicalProceduresList", [])

        for proс_id in med_proc_list:
            proc = get_object_or_404(MedicalProcedures, pk=proс_id)
            cate_proc = CategoriesProcedures.objects.create(Category_ID=med_cat, Procedure_ID=proc)
            med_cat.MedicalProceduresList.add(proc)

        if not med_proc_list:
            med_cat.MedicalProceduresList.clear()

        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # status = request.data.get("Status")

@api_view(['Put'])
def put_MedCat_moderator(request, id, format=None):
    """
    Модератор обновляет информацию о мед. категории (заявка)
    """

    # med_cat = MedicalCategories.objects.get(MedicalCategories_ID=id)
    #
    # status = request.data.get("Status")
    #
    # if status in ["w", "e", "c"]:
    #     med_cat.Status = status
    #     med_cat.save()
    #     serializer = MC_Serializer(med_cat)
    #     return Response(serializer.data)
    #
    # else:
    #     return Response("Доступ запрещен")

    med_cat = get_object_or_404(MedicalCategories, pk=id)
    serializer = MC_Serializer(med_cat, data=request.data, partial=True)
    if serializer.is_valid():
        status = request.data.get("Status")
        status = status if status else med_cat.Status

        if status in ["w", "e", "c"]:
            med_cat.Status = status
        else:
            return Response("Доступ запрещен")

        serializer.save()

        med_proc_list = request.data.get("MedicalProceduresList", [])
        for proс_id in med_proc_list:
            proc = get_object_or_404(MedicalProcedures, pk=proс_id)
            cate_proc = CategoriesProcedures.objects.create(Category_ID=med_cat, Procedure_ID=proc)
            med_cat.MedicalProceduresList.add(proc)

        if not med_proc_list:
            med_cat.MedicalProceduresList.clear()

        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get'])
def get_MedCat(request, id, format=None):
        """
        Возвращает одну медицинскую категорию (заявку)
        """
        med_cat = get_object_or_404(MedicalCategories, MedicalCategories_ID=id)
        serializer = MC_Serializer(med_cat)
        return Response(serializer.data)


@api_view(['Delete'])
def del_MedCat(request, id, id2, format=None):
    """
    Удаляет процедуру из категории
    """
    med_cat = MedicalCategories.objects.get(MedicalCategories_ID=id)
    cat_proc = get_object_or_404(CategoriesProcedures,Category_ID=id, Procedure_ID=id2)
    cat_proc.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['Delete'])
# def delete_MedProc(request, id, format=None):
#     """
#     Удаление процедуры
#     """
#     med_proc = MedicalProcedures.objects.get(Procedure_ID=id)
#
#     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['Get'])
def get_ProcCat(request, format=None):
    """
    Получаем связь м-м
    """
    cat_proc = CategoriesProcedures.objects.all()

    if not cat_proc:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CP_Serializer(cat_proc, many=True)

    return Response(serializer.data)

@api_view(['Delete'])
def deleteCategory(request, id, format=None):
    """
    Удаление категории (заявки)
    """
    try:
        med_cat = MedicalCategories.objects.get(MedicalCategories_ID=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        med_cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Post'])
def create_MedCat(request, format=None):
    """
    Создание категории (заявки)
    """
    serializer = MC_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        med_cat = get_object_or_404(MedicalCategories, pk=request.data.get("MedicalCategories_ID"))
        med_proc_list = json.loads(request.data.get("MedicalProceduresList", []))
        for proс_id in list(med_proc_list):
            proc = get_object_or_404(MedicalProcedures, pk=proс_id)
            cate_proc = CategoriesProcedures.objects.create(Category_ID=med_cat, Procedure_ID=proc)
            med_cat.MedicalProceduresList.add(proc)

        if not med_proc_list:
            med_cat.MedicalProceduresList.clear()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get'])
def mcFilter(request, format=None):
    """
    Фильтр по имени
    """

    nameFilter = request.GET.get('Category_Name')

    if nameFilter:
        data = MedicalCategories.objects.filter(Category_Name__icontains=nameFilter)
        if not data:
            return Response("Не найдено по фильтру")
        serializer = MC_Serializer(data, many=True)
        return Response(serializer.data)
    else:
        return Response("Не найдено")