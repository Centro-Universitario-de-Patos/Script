from django.db import models

class Moodle(models.Model):
    username = models.CharField("Username", max_length=254)
    password = models.CharField("Senha", max_length=254)
    firstname = models.CharField("Primeiro", max_length=254)
    lastname = models.CharField("Sobrenome", max_length=254)
    email = models.CharField("Email", max_length=254)
    course1 = models.CharField("Disciplina", max_length=254)
    


