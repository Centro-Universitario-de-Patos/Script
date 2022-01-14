from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Moodle

@admin.register(Moodle)
class MoodleAdmin(ImportExportModelAdmin):
    list_display = ('username', 'password', 'firstname', 'lastname', 'email', 'course1', )

