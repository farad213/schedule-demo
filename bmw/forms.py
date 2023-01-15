from django import forms
from .models import Technician, Customer


class Length_form(forms.Form):
    ccs = forms.CharField(max_length=10, required=False)
    vvs = forms.CharField(max_length=10, required=False)

    ccs.widget.attrs = {"class": "ccs", "id": "ccs", "placeholder": "Cölöpcsúcs szint", "autocomplete": "off"}
    vvs.widget.attrs = {"class": "vvs", "id": "vvs", "placeholder": "Visszavésési szint", "autocomplete": "off"}


class Buildings_form(forms.Form):
    sorszam = forms.CharField(max_length=10, required=False)
    building = forms.ChoiceField(choices=[("TMO", "TMO"), ("TKB", "TKB"), ("TU", "TU"), ("TEM", "TEM")], widget=forms.RadioSelect)

    sorszam.widget.attrs = {"class": "sorszam", "id": "sorszam", "placeholder": "Sorszám", "autocomplete": "off"}



class TechnicianChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class CustomerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class QuickReportForm(forms.Form):
    language = forms.ChoiceField(choices=[("HU", "HU"), ("EN", "EN")], widget=forms.RadioSelect)
    customer = CustomerChoiceField(queryset=Customer.objects.all(), empty_label=None)
    date_of_measurement = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    technician = TechnicianChoiceField(queryset=Technician.objects.all(), widget=forms.RadioSelect)
    building = forms.ChoiceField(choices=[("TEM", "TEM"), ("TMO", "TMO"), ("TKB", "TKB"), ("TU", "TU"), ("Other", "Other")])
    comment = forms.CharField(required=False, widget=forms.Textarea)
    profile_from = forms.IntegerField(required=False)
    profile_to = forms.IntegerField(required=False)


    profile_from.widget.attrs = {"class": "profile_from"}
    profile_to.widget.attrs = {"class": "profile_to"}
    comment.widget.attrs = {"placeholder": "Komment"}
    date_of_measurement.widget.attrs = {"placegolder": "Mérés napja"}