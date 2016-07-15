from .models import Menu, Order
from rest_framework import serializers
from datetime import datetime

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(style={'type': 'textarea'}, default='test')


    class Meta:
        model = Order
        fields = "__all__"

    # def validate(self, data):
    #     if data['title'].date_day != datetime.now().date():
    #         raise serializers.ValidationError("err")
    #     return data

    def validate_title(self, value):

        if value.date_day != datetime.now().date():
            raise serializers.ValidationError("Meniul este gresit!")
        return value

    def validate_phone(self, value):
        # for i in value:
        if not value.isnumeric():
            raise serializers.ValidationError("Error phone")
        return value
    def validate_email(self, value):
        # for i in value:
        if '@' not in value[1:len(value)-1]:
            raise serializers.ValidationError("Error email")
        return value
    # def validate_phone(self, value):
    #     if phone.isalnum():
    #         raise serializers.ValidationError("Numarul de telefon este incorect")
    #     # return valuedef validate_title(self, value):
    #     return phone

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status', 'title')

