from django import forms
from .models import DateBoundWithProject, Vehicle, Artifact, Profile, Subproject, User, Date
from django.contrib.auth.models import User


class DateBoundWithProjectForm(forms.ModelForm):

    class Meta:
        model = DateBoundWithProject
        fields = ["subproject", "artifact", "profile", "employee", "vehicle", "comment"]

    employee = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name="Schedule - Monitoring"), widget=forms.CheckboxSelectMultiple)
    vehicle = forms.ModelMultipleChoiceField(queryset=Vehicle.objects.all(), widget=forms.CheckboxSelectMultiple)
    profile = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=forms.SelectMultiple, required=False)
    artifact = forms.ModelChoiceField(queryset=Artifact.objects.all(), widget=forms.Select, required=True)
    subproject = forms.ModelChoiceField(queryset=Subproject.objects.all(), widget=forms.Select, required=True)
    def __init__(self, date, *args, **kwargs):
        super().__init__(*args, **kwargs)

        all_possible_employees = User.objects.filter(groups__name="Schedule - Monitoring")
        employees_on_leave = Date.objects.get(date=date).employees_on_leave.all()
        available_employees = [employee.id for employee in all_possible_employees if employee not in employees_on_leave]

        self.fields['employee'].label_from_instance = self.label_from_instance_employee
        self.fields['vehicle'].label_from_instance = self.label_from_instance_vehicle
        self.fields["employee"].queryset = User.objects.filter(id__in=available_employees)
        self.fields['artifact'].queryset = Artifact.objects.none()
        self.fields['profile'].queryset = Profile.objects.none()

        self.fields['artifact'].required = False
        self.fields['profile'].required = False
        self.fields['subproject'].required = False

        if 'subproject' in self.data:
            try:
                subproject_id = int(self.data.get('subproject'))
                self.fields['artifact'].queryset = Artifact.objects.filter(subproject_id=subproject_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty artifact queryset
        # elif self.instance.pk:
        #     self.fields['artifact'].queryset = self.instance.subproject.artifact_set

        if 'artifact' in self.data:
            try:
                artifact_id = int(self.data.get('artifact'))
                self.fields['profile'].queryset = Profile.objects.filter(artifact_id=artifact_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty profile queryset
        # elif self.instance.pk:
        #     self.fields['profile'].queryset = self.instance.artifact.profile_set

    def label_from_instance_employee(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def label_from_instance_vehicle(self, obj):
        return f"{obj.vehicle_name}({obj.license_plate})"

class ExportDates(forms.Form):
    start = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
