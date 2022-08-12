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
import datetime

def converter(request):

    dados = {
        'conteudo_disciplina_jsons': retorna_api('https://apidisfip.herokuapp.com/disciplina/?format=json'),
    }
    li = []
    for dt in dados['conteudo_disciplina_jsons']:
        for d in dt:
            dd = dt[d]
            matriz = dt['matriz']
            li.append(matriz)

    lista = remove_repetidos(li)
    semestre = data_atual()
    dados = {
        'semestre':semestre,
        'conteudo_disciplina_jsons': retorna_api('https://apidisfip.herokuapp.com/disciplina/?format=json'),
        'lista': lista,
        'curso':''
    }
    if request.method == 'POST':
        moodle = Moodle.objects.all()
        moodle_resource = MoodleResource()
        dataset = Dataset()

        try:
            new_arquivo = request.FILES['file']
            a = str(new_arquivo)
            print(new_arquivo)
            print(a[-3:])
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
            print('')
        except:
            return render(request, 'conversor/converter_erro.html', dados)
            
        nome_disciplina = request.POST['nome-disciplina']

        if nome_disciplina == "Escolha Uma Disciplina" or nome_disciplina == 'default':

            return render(request, 'conversor/converter_erro.html', dados)


        if a[-3:] == "lsx":
            try:
                imported_data = dataset.load(new_arquivo.read(), format = 'xlsx')
            except:
                return render(request, 'conversor/converter_erro.html', dados)

        elif a[-3:] == 'xls':
            try:
                imported_data = dataset.load(new_arquivo.read(), format = 'xls')
            except:
                return render(request, 'conversor/converter_erro.html', dados)
        else:
            return render(request, 'conversor/converter_erro.html', dados)

        # try:
        #     imported_data = dataset.load(new_arquivo.read(), format = 'xls')
        #     api_disciplinas = retorna_api('https://apidisfip.herokuapp.com/disciplina/?format=json')        
        # except :
        #     return render(request, 'conversor/converter_erro.html', dados)
 

 
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
    conteudo_disciplina_jsons = retorna_api('https://apidisfip.herokuapp.com/disciplina/?format=json'),
    dados = {
        'conteudo_disciplina_jsons':conteudo_disciplina_jsons,
    }
    moodles = Moodle.objects.all()
    nome = moodles[0].course1
    nome_formatado = nome[(nome.find('-')+1):-4]
    response = HttpResponse(content_type = 'text/csv')

    data_e_hora_atuais = datetime.datetime.now()

    print(nome_formatado)
    try:        

        data = str(data_e_hora_atuais.strftime('%d/%m/%Y %H:%M'))
        
        print(data)
        response['Content-Disposition'] = 'attachment; filename=' + nome_formatado +'_' + data + '.csv'
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
    semestre = data_atual()
    dados = {
        
        'conteudo_disciplina_jsons': retorna_api('https://apidisfip.herokuapp.com/disciplina/?format=json'),
    
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
            curso = 'SERVIÇO SOCIAL'
        print(curso)
        l = []
        # print(dados['conteudo_disciplina_jsons'][0]['tipo'])
        for dt in dados['conteudo_disciplina_jsons']:
            for d in dt:
                dd = dt[d]

                if str(dd).title() == curso.title():
                    nome_disciplina = dt['nome_disciplina']
                    matricula = dt['matricula']
                    dis_formatada = f'{matricula} - {nome_disciplina}'
                    l.append(dis_formatada)
    print(l)

    data = { 
        'semestre':semestre,
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

def data_atual():
    data = datetime.date.today()
    ano = data.strftime("%Y")
    mes = data.strftime("%m")
    if int(mes) > 6:
        semestre = 2
    else:
        semestre = 1
    
    return f'{ano[2:]}.{semestre}'

    
