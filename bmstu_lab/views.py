import django.db.models.base
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from bmstu_lab.models import MedicalProcedures
from django.template.defaultfilters import linebreaksbr
import psycopg2

def GetProcedure(request, id):
    data = MedicalProcedures.objects.filter(Procedure_ID=id).values()
    return render(request, 'order.html', data)

def filter(request):
    del_id = request.GET.get('delete')
    if (del_id != None):
        change_status(del_id)
        data = {'data': MedicalProcedures.objects.filter(Status='1').values()}
        return render(request, "filter.html", data)

    data = {'data': MedicalProcedures.objects.values()}
    if (request.GET.get('filter') is not None):
        search = request.GET.get('filter')
        data_filter = {'data': MedicalProcedures.objects.filter(Procedure_Name__icontains=search)}
        print(data_filter)
        return render(request, 'filter.html', data_filter)
    else:
        return render(request, 'filter.html', data)


def change_status(id):
    conn = psycopg2.connect(dbname="medicine", host="localhost", user="postgres", password="adminros", port="5432")
    cursor = conn.cursor()
    cursor.execute('''UPDATE public.bmstu_lab_medicalprocedures 
                      set "Status"='0' 
                      where "Procedure_ID"=%s''',(id))

    conn.commit()
    cursor.close()
    conn.close()


def deleteProcedure(request):
    return None