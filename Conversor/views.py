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

    dados = {
        'conteudo_disciplina_jsons': retorna_api('https://glacial-oasis-62433.herokuapp.com/disciplina/?format=json'),
    }
    li = []
    for dt in dados['conteudo_disciplina_jsons']:
        for d in dt:
            dd = dt[d]
            matriz = dt['matriz']
            li.append(matriz)

    lista = remove_repetidos(li)
    print(lista)
    print(lista)
    print(lista)
    print(lista)
    dados = {
        'conteudo_disciplina_jsons': retorna_api('https://glacial-oasis-62433.herokuapp.com/disciplina/?format=json'),
        'lista': lista,
        'curso':''
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
    conteudo_disciplina_jsons = retorna_api('https://glacial-oasis-62433.herokuapp.com/disciplina/?format=json'),
    dados = {
        'conteudo_disciplina_jsons':conteudo_disciplina_jsons,
    }
    try:        
        moodles = Moodle.objects.all()
        nome = moodles[0].course1
        nome_formatado = nome[(nome.find('-')+1):]
        response = HttpResponse(content_type = 'text/csv')

        response['Content-Disposition'] = 'attachment; filename=' + nome_formatado   + '.csv'
        writer = csv.writer(response)
        writer.writerow(['username', 'password','firstname', 'lastname','email', 'course1'])
        for moodle in moodles:
            codigo = moodle.course1[0:(moodle.course1.find('-')-1)]
            writer.writerow([moodle.username, moodle.password, moodle.firstname, moodle.lastname, moodle.email, codigo])
            moodle.delete()
        return response
    except:
        return render(request, 'conversor/converter_erro.html', dados)
    

def retorna_api(url):
    conteudo = requests.get(url)
    conteudo_json = conteudo.json()
    return conteudo_json

def retorna_curso(request):
    dados = {
        'conteudo_disciplina_jsons': retorna_api('https://glacial-oasis-62433.herokuapp.com/disciplina/?format=json'),
    
    }

    li = []
    for dt in dados['conteudo_disciplina_jsons']:
        for d in dt:
            dd = dt[d]
            matriz = dt['matriz']
            li.append(matriz)

    lista = remove_repetidos(li)


    if request.method == "POST":

        curso = request.POST['curso']
        if curso == 'Serviço Social':
            curso = 'SS2018.1'
        print(curso)
        l = []
        # print(dados['conteudo_disciplina_jsons'][0]['tipo'])
        for dt in dados['conteudo_disciplina_jsons']:
            for d in dt:
                dd = dt[d]

                if dd == curso:
                    nome_disciplina = dt['nome_disciplina']
                    matricula = dt['matricula']
                    dis_formatada = f'{matricula} - {nome_disciplina}'
                    l.append(dis_formatada)
    print(l)

    data = { 
        'curso': curso,
        'l' : l,
        'lista': lista,
    }
    return render(request, 'conversor/converter.html', data)


def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

