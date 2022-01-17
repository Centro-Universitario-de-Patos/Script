from asyncore import write
from datetime import datetime
from django.shortcuts import render
from .models import Moodle
from .resources import MoodleResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
import csv
def converter(request):
    print(request.method)
    if request.method == 'POST':
        moodle_resource = MoodleResource()
        dataset = Dataset()
        new_arquivo = request.FILES['file']
        nome_disciplina = request.POST['nome-disciplina']
        imported_data = dataset.load(new_arquivo.read(), format = 'xlsx')
        for data in imported_data:
            nome_e_sobrenome = data[1].split(' ')
            nome = data[1].split(' ')[0]
            sobrenome = str(data[1].split(' ')[1:])
            sobrenome = sobrenome.replace(',', ' ')
            sobrenome = sobrenome.replace('[', '')
            sobrenome = sobrenome.replace(']', '')
            sobrenome = sobrenome.replace("'", '')
            primeiro_nome = str([data[1].split(None,1)[0]])[2:-2]
            
            value = Moodle(
                
                username = data[2],
                password = 'changeme',
            
                firstname = nome,
                lastname = sobrenome,
                email = data[2],
                course1 = nome_disciplina,
            )
            value.save()
        return render(request, 'conversor/converter.html')
    else:
        return render(request, 'conversor/converter.html')
    
def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['username', 'password','firstname', 'lastname','email', 'course1'])
    
    moodles = Moodle.objects.all()
    for moodle in moodles:
        writer.writerow([moodle.username, moodle.password, moodle.firstname, moodle.lastname, moodle.email, moodle.course1])
    
    return response