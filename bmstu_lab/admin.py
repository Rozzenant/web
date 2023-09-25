from django.contrib import admin
from .models import *


admin.site.register(Users)
admin.site.register(MedicalCategories)
admin.site.register(MedicalProcedures)
admin.site.register(CategoriesProcedures)

