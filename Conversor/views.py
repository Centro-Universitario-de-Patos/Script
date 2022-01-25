from ast import Try
from asyncore import write
from datetime import datetime
from email.policy import default
from django.shortcuts import render
from .models import Moodle
from .resources import MoodleResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
import csv
import requests

def converter(request):
    print(request.method)
    dados = {
        'conteudo_disciplina_jsons': retorna_api('https://glacial-oasis-62433.herokuapp.com/disciplina/?format=json'),
    }
    if request.method == 'POST':
        moodle = Moodle.objects.all()
        moodle_resource = MoodleResource()
        dataset = Dataset()

        try:
            new_arquivo = request.FILES['file']
        except:
            return render(request, 'conversor/converter_erro.html', dados)
            
        nome_disciplina = request.POST['nome-disciplina']

        if nome_disciplina == "Escolha Uma Disciplina" or nome_disciplina == 'default':

            return render(request, 'conversor/converter_erro.html', dados)


        try:
            imported_data = dataset.load(new_arquivo.read(), format = 'xlsx')
            api_disciplinas = retorna_api('https://glacial-oasis-62433.herokuapp.com/disciplina/?format=json')        
        except:
            return render(request, 'conversor/converter_erro.html', dados)
 
        print(nome_disciplina)

        

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
            tamanhoBD = len(moodle)
            if tamanhoBD == 0:
                value.save()

            else:
                cadastrado = Moodle.objects.filter(username=data[2])
                if cadastrado == 0:
                    value.save() 
        return render(request, 'conversor/converter_certo.html', dados)

    else:
        return render(request, 'conversor/converter.html', dados)
    
def export_csv(request):
    dados = {
        'conteudo_disciplina_jsons': retorna_api('https://glacial-oasis-62433.herokuapp.com/disciplina/?format=json'),
    }
    try:        
        moodles = Moodle.objects.all()
        nome = moodles[0].course1
        print(nome)
        response = HttpResponse(content_type = 'text/csv')

        response['Content-Disposition'] = 'attachment; filename=' + nome + '.csv'
        writer = csv.writer(response)
        writer.writerow(['username', 'password','firstname', 'lastname','email', 'course1'])
        
        for moodle in moodles:
            writer.writerow([moodle.username, moodle.password, moodle.firstname, moodle.lastname, moodle.email, moodle.course1])
            moodle.delete()
        return response
    except:
        return render(request, 'conversor/converter_erro.html', dados)
    

def retorna_api(url):
    conteudo = requests.get(url)
    conteudo_json = conteudo.json()
    return conteudo_json

