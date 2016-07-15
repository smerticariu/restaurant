from django import forms
from .models import Menu,Order
import datetime



class MenuForm(forms.ModelForm):

    # date_day = forms.DateField(widget=forms.SelectDateWidget())
    date_day = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        # self.fields['date_day'].required=True
        self.fields['title'].widget = forms.TextInput(attrs={'placeholder':'titlul meniului'})
        self.fields['date_day'].widget = forms.TextInput(attrs={'placeholder':'Introduceti data'})
        self.fields['date_day'].initial = datetime.datetime.now().date()
        self.fields['dish1'].widget = forms.TextInput(attrs={'placeholder':'Introduceti felul 1'})
        self.fields['dish2'].widget = forms.TextInput(attrs={'placeholder':'Introduceti felu 2'})
        self.fields['desert'].widget = forms.TextInput(attrs={'placeholder':'Introduceti desertul'})


        # self.fields['date_day'].initial = datetime.datetime.now

    class Meta:
        model = Menu
        fields = ('__all__')

    def clean(self):
        # cleaned_data = self.cleaned_data
        cleaned_data = self.cleaned_data,

    def clean_date_day(self):
        date_day_string = self.cleaned_data['date_day']
        try:
            date_day = datetime.datetime.strptime(date_day_string, '%Y-%m-%d').date()
        except Exception, e:
            raise forms.ValidationError("Data nu are formatul corect!")


        if date_day < datetime.date.today():
            raise forms.ValidationError("Data nu poate fi din trecut!")
        return date_day


class OrderForm(forms.ModelForm):

    date_order = forms.DateField(widget=forms.SelectDateWidget())

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['date_order'].required=True
        self.fields['title'].help_text = 'Introduceti titlul meniului'
        self.fields['name'].help_text = 'Introduceti numele'
        self.fields['email'].help_text = 'Introduceti email'
        self.fields['phone'].help_text = 'Introduceti numarul de telefon'
        self.fields['adress'].help_text = 'Introduceti adresa'
        self.fields['raiting'].help_text = 'Introduceti raiting-ul'
        self.fields['date_order'].initial = datetime.datetime.now

    class Meta:
        model = Order
        fields = ('__all__')

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data


    def clean_date_order(self):
        date_order = self.cleaned_data['date_order']
        if date_order < datetime.date.today():
            raise forms.ValidationError("Data nu poate fi din trecut!")
        return date_order

