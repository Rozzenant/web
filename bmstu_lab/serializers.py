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

        # if instance.Date_Creation is not None:
        #     if show_time:
        #         # representation['Date_Creation'] = instance.Date_Creation.strftime('%Y-%m-%d %H:%M:%S')
        #         pass
        #     else:
        #         representation['Date_Creation'] = instance.Date_Creation.strftime('%Y-%m-%d')
        #
        # if instance.Date_Approving is not None:
        #     if show_time:
        #         # representation['Date_Approving'] = instance.Date_Approving.strftime('%Y-%m-%d %H:%M:%S')
        #         pass
        #     else:
        #         representation['Date_Approving'] = instance.Date_Approving.strftime('%Y-%m-%d')
        #
        # if instance.Date_End is not None:
        #     if show_time:
        #         # representation['Date_End'] = instance.Date_End.strftime('%Y-%m-%d %H:%M:%S')
        #         pass
        #     else:
        #         representation['Date_End'] = instance.Date_End.strftime('%Y-%m-%d')


        return representation

    class Meta:
        model = Trauma
        fields = ['Trauma_ID',
                  'Status',
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
