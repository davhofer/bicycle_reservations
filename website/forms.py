from django import forms
class InputForm(forms.Form):
    start = forms.CharField(max_length=50)
    dest = forms.CharField(max_length=50)
    time = forms.TimeField()
    date = forms.DateField()