from django import forms


class Length_form(forms.Form):
    ccs = forms.CharField(max_length=10, required=False)
    vvs = forms.CharField(max_length=10, required=False)

    ccs.widget.attrs = {"class": "ccs", "id": "ccs", "placeholder": "Cölöpcsúcs szint", "autocomplete": "off"}
    vvs.widget.attrs = {"class": "vvs", "id": "vvs", "placeholder": "Visszavésési szint", "autocomplete": "off"}


class Buildings_form(forms.Form):
    sorszam = forms.CharField(max_length=10, required=False)
    building = forms.ChoiceField(choices=[("TMO", "TMO"), ("TKB", "TKB")], widget=forms.RadioSelect)

    sorszam.widget.attrs = {"class": "sorszam", "id": "sorszam", "placeholder": "Sorszám", "autocomplete": "off"}
