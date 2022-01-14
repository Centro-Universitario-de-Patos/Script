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
        imported_data = dataset.load(new_arquivo.read(), format = 'xlsx')
        for data in imported_data:
            
            value = Moodle(
                username = data[0],
                password = data[1],
                firstname = data[2],
                lastname = data[0],
                email = data[1],
                course1 = data[2],
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