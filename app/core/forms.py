from datetime import datetime, date
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *
from phonenumber_field.formfields import PhoneNumberField


class BuyerInfoForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={
                "placeholder": ("email@gmail.com"),
                "id": "phone",
            }
        ),
    )
    phone = PhoneNumberField(
        label=_("Телефон"),
        widget=forms.TextInput(
            attrs={
                "placeholder": ("+380 __ ___ __ __"),
                "id": "email",
            }
        ),
    )


class PassagerInfoForm(forms.Form):
    first_name = forms.CharField(
        label=_("Ім'я"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "first_name",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Фамілія"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "last_name",
            }
        ),
    )


class CitySelectionForm(forms.Form):
    start_point = forms.CharField(
        label=_("Звідки"),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "id": "search_data_start_point",
            }
        ),
    )
    end_point = forms.CharField(
        label=_("Куди"),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "id": "search_data_end_point",
            }
        ),
    )
    date = forms.DateField(
        label=_("Дата поїздки"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control datepicker",
                "id": "floatingInputGrid",
                "min": datetime.now().date(),
                "value": datetime.now().strftime("%Y-%m-%d"),
            }
        ),
    )
    passengers_quantity = forms.IntegerField(
        label=_("Кількість пасажирів"),
        min_value=0,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "type": "number",
                "class": "form-control number-input",
                "id": "floatingInputGrid",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_point = cleaned_data.get("start_point")
        end_point = cleaned_data.get("end_point")

        if start_point and end_point and start_point == end_point:
            raise ValidationError(_("Початковий та кінцевий пункт мають бути різними."))

        return cleaned_data
