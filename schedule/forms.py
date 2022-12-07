from django import forms
from .models import DateBoundWithProject, Employee, Vehicle

class DateBoundWithProjectForm(forms.ModelForm):

    class Meta:
        model = DateBoundWithProject
        fields = ["employee", "vehicle", "comment"]

    employee = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), widget=forms.CheckboxSelectMultiple)
    vehicle = forms.ModelMultipleChoiceField(queryset=Vehicle.objects.all(), widget=forms.CheckboxSelectMultiple)