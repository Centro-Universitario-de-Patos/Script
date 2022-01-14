import imp
from import_export import resources
from .models import Moodle 

class MoodleResource(resources.ModelResource):
    class meta:
        model = Moodle