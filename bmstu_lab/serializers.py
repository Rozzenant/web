from bmstu_lab.models import First_aid, Trauma, First_aid_Trauma
from rest_framework import serializers


class First_aid_Serializer(serializers.ModelSerializer):

    class Meta:
        model = First_aid
        fields = ['First_aid_ID',
                  'First_aid_Name',
                  'Description',
                  'Image_URL',
                  'Price']




class Trauma_Serializer(serializers.ModelSerializer):
    Creator_Name = serializers.SerializerMethodField()
    Moderator_Name = serializers.SerializerMethodField()
    First_aid_in_Trauma_List = First_aid_Serializer(many=True)

    @staticmethod
    def get_Creator_Name(obj):
        return obj.Creator.Username if obj.Creator else None

    @staticmethod
    def get_Moderator_Name(obj):
        return obj.Moderator.Username if obj.Moderator else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # show_time = self.context.get('show_time', True)
        show_traumas = self.context.get('show_traumas', True)

        if not show_traumas:
            representation.pop('First_aid_in_Trauma_List', None)


        return representation

    class Meta:
        model = Trauma
        fields = ['Trauma_ID',
                  'Status',
                  'Confirmation_Doctor',
                  'Creator_Name',
                  'Moderator_Name',
                  'Date_Creation',
                  'Date_Approving',
                  'Date_End',
                  'First_aid_in_Trauma_List'
                  ]


class First_aid_Trauma_Serializer(serializers.ModelSerializer):
    class Meta:
        model = First_aid_Trauma
        fields = '__all__'
