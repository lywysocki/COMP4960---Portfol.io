from django import forms
from django.core.validators import RegexValidator


class InputForm(forms.Form):
    HIST_TFS = [
        ('5yH', '5 Years'),
        ('1yH', '1 Year'),
        ('6mH', '6 Months'),
        ('1mH', '1 Month'),
    ]
    FUTURE_TFS = [
        ('1yF', '1 Year'),
        ('6mF', '6 Months'),
        ('3mF', '3 Months'),
        ('1mF', '1 Month'),
    ]
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    ticker = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'inputstyle', 'style':'height:30px;width:35%;font-size:large;'}),
        validators=[alphanumeric]
        )
    hist = forms.ChoiceField(
        choices=HIST_TFS,
        widget=forms.RadioSelect(attrs={'class': 'inputstyle', 'style': 'height:100%;'}),
        initial="1yH",
    )
    future = forms.ChoiceField(
        choices=FUTURE_TFS,
        widget=forms.RadioSelect(attrs={'class': 'inputstyle', 'style': 'height:100%;'}),
        initial="1mF",
    )