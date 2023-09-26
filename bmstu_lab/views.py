# import django.db.models.base
# from django.shortcuts import render
# from django.http import HttpResponse
from django.shortcuts import render
from bmstu_lab.models import MedicalProcedures
from django.template.defaultfilters import linebreaksbr
import psycopg2

RESET = True

def GetProcedure(request, id):
    data = {'data': MedicalProcedures.objects.filter(Procedure_ID=id).values()[0]}
    data['data']['Description'] = linebreaksbr(data['data']['Description']) # add indents to the text, as in the database
    return render(request, 'procedure.html', data)

def main(request):
    if (request.GET.get('reset') is not None):
        resetStatus()
    data = {'data': MedicalProcedures.objects.order_by('Procedure_ID').filter(Status='1')}
    if (request.GET.get('filter') is not None):
        search = request.GET.get('filter')
        data_filter = {'data': MedicalProcedures.objects.filter(Procedure_Name__icontains=search).filter(
            Status='1').order_by(
            'Procedure_ID')}
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