from bmstu_lab.models import MedicalProcedures, MedicalCategories, CategoriesProcedures
from rest_framework import serializers

from bmstu_lab.models import MedicalProcedures, MedicalCategories, CategoriesProcedures
from rest_framework import serializers


class MP_Serializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProcedures
        fields = '__all__'

class MC_Serializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCategories
        fields = '__all__'

class CP_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesProcedures
        fields = '__all__'