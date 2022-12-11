from django import forms
from .models import DateBoundWithProject, Employee, Vehicle, Artifact, Profile, Subproject



class DateBoundWithProjectForm(forms.ModelForm):

    class Meta:
        model = DateBoundWithProject
        fields = ["subproject", "artifact", "profile", "employee", "vehicle", "comment"]

    employee = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), widget=forms.CheckboxSelectMultiple)
    vehicle = forms.ModelMultipleChoiceField(queryset=Vehicle.objects.all(), widget=forms.CheckboxSelectMultiple)
    profile = forms.ModelMultipleChoiceField(queryset=Profile.objects.none(), widget=forms.SelectMultiple, required=False)
    artifact = forms.ModelChoiceField(queryset=Artifact.objects.none(), widget=forms.Select, required=True)
    subproject = forms.ModelChoiceField(queryset=Subproject.objects.all(), widget=forms.Select, required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['artifact'].queryset = Artifact.objects.none()

        self.fields['artifact'].required = False
        self.fields['profile'].required = False
        self.fields['subproject'].required = False

        if 'subproject' in self.data:
            try:
                subproject_id = int(self.data.get('subproject'))
                self.fields['artifact'].queryset = Artifact.objects.filter(subproject_id=subproject_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty artifact queryset
        elif self.instance.pk:
            self.fields['artifact'].queryset = self.instance.subproject.artifact_set

        if 'artifact' in self.data:
            try:
                artifact_id = int(self.data.get('artifact'))
                self.fields['profile'].queryset = Profile.objects.filter(artifact_id=artifact_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty profile queryset
        elif self.instance.pk:
            self.fields['profile'].queryset = self.instance.artifact.profile_set