from django.test import TestCase

# Create your tests here.

from django.views.static import serve 
import os 
def get(request, obj_id):

    recipe = RecipeModel.objects.get(id=obj_id)
    file_path = recipe.image.path 
    return serve(request, os.path.basename(file_path), os.path.dirname(file_path))