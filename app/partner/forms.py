from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from django_select2.forms import ModelSelect2Widget

from core.models import Bus, Company, Trip, Station, City


class CompanyForm(forms.ModelForm):
    company_name = forms.CharField(
        label="Назва компанії", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Company
        fields = ("company_name",)


class CreateBusForm(forms.ModelForm):
    brand = forms.CharField(
        max_length=255,
        label=_("Опис"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingSelect",
            }
        ),
    )
    number_of_seats = forms.IntegerField(
        label=_("Кількість місць"),
        min_value=1,
        max_value=100,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "type": "number",
                "class": "form-control number-input",
                "id": "floatingSelect",
            }
        ),
    )
    licence_plate = forms.CharField(
        label=_("Реєстраційний номер"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingSelect",
                "placeholder": "AA5555BB",
            }
        ),
    )

    class Meta:
        model = Bus
        fields = ("licence_plate", "number_of_seats", "brand")

    def clean(self):
        cleaned_data = super().clean()
        licence_plate = cleaned_data.get("licence_plate")

        if " " in str(licence_plate):
            raise ValidationError(
                {"licence_plate": "Номерний знак не повинен містити знаків відступу."}
            )

        return cleaned_data


class CreateUpdateTripForm(forms.ModelForm):
    timedate_departure = forms.DateTimeField(
        label=_("Дата/Час відправки"),
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "id": "timedate_departure",
            }
        ),
    )
    timedate_arrival = forms.DateTimeField(
        label=_("Дата/Час приїзду"),
        widget=DateTimePickerInput(
            attrs={
                "class": "form-control",
                "id": "timedate_arrival",
            }
        ),
    )
    price = forms.IntegerField(
        label=_("Ціна"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "id": "price",
            }
        ),
    )
    departure_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        label=_("Станція відправки"),
        empty_label="",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "departure_station",
            }
        ),
    )
    start_point = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=_("Місто відправки"),
        widget=ModelSelect2Widget(
            model=City,
            search_fields=["city__icontains"],
            attrs={
                "class": "form-select",
                "id": "start_point",
            },
        ),
    )
    arrival_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        label=_("Станція прибуття"),
        empty_label="",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "arrival_station",
            }
        ),
    )
    end_point = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=_("Місто прибуття"),
        widget=ModelSelect2Widget(
            model=City,
            search_fields=["city__icontains"],
            attrs={
                "class": "form-select",
                "id": "end_point",
            },
        ),
    )

    class Meta:
        model = Trip
        fields = [
            "bus",
            "start_point",
            "departure_station",
            "timedate_departure",
            "end_point",
            "arrival_station",
            "timedate_arrival",
            "price",
        ]

    def __init__(self, user, *args, **kwargs):
        super(CreateUpdateTripForm, self).__init__(*args, **kwargs)
        self.fields["bus"].queryset = Bus.objects.select_related("company").filter(
            company__partner__user=user
        )
        self.fields["bus"].widget.attrs.update(
            {
                "class": "form-select",
            }
        )
        self.fields["bus"].empty_label = ""

    def clean(self):
        cleaned_data = super().clean()
        timedate_departure = cleaned_data.get("timedate_departure")
        timedate_arrival = cleaned_data.get("timedate_arrival")

        if timedate_departure and timedate_arrival:
            if timedate_departure >= timedate_arrival:
                raise ValidationError(
                    _("Дата приїзду повинна бути більша ніж дата від'їзду.")
                )

        return cleaned_data


class StationCreateFrom(forms.ModelForm):
    station = forms.CharField(
        label=_("Назва станції"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Школа №1",
                "class": "form-control",
                "id": "station",
            }
        ),
    )

    street_type = forms.CharField(
        label=_("Тип"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Вулиця/Провулок",
                "class": "form-control",
                "id": "street_type",
            }
        ),
    )

    street = forms.CharField(
        label=_("Назва"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Котляревського",
                "class": "form-control",
                "id": "street",
            }
        ),
    )

    number = forms.CharField(
        label=_("Номер"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "18",
                "class": "form-control",
                "id": "number",
            }
        ),
        validators=[
            RegexValidator(
                regex=r"^[0-9-]+$",
                message=_("Дозволені тільки цифри та тире."),
                code="invalid_number",
            ),
        ],
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=_("Місто"),
        empty_label="",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "city",
            }
        ),
    )

    class Meta:
        model = Station
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        street_type = cleaned_data.get("street_type")
        street = cleaned_data.get("street")
        number = cleaned_data.get("number")
        city = cleaned_data.get("city")

        if Station.objects.filter(
            street_type=street_type, street=street, number=number, city=city
        ).exists():
            raise ValidationError(
                _(f"Станція з такою адресою вже існує в місті {city.city}")
            )

    def __init__(self, *args, **kwargs):
        station_value = kwargs.pop("station", None)
        street_type_value = kwargs.pop("street_type", None)
        street_value = kwargs.pop("street", None)
        number_value = kwargs.pop("number", None)
        city_value = kwargs.pop("city", None)

        # Call the super().__init__ method to initialize the form
        super(StationCreateFrom, self).__init__(*args, **kwargs)

        # Set initial values for the fields based on the provided parameters
        self.fields["station"].initial = station_value
        self.fields["street_type"].initial = street_type_value
        self.fields["street"].initial = street_value
        self.fields["number"].initial = number_value
        self.fields["city"].initial = city_value


class TripSearchForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={"class": "form-control", "id": "id"},
        )
    )
    start_point = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=_("Звідки"),
        empty_label=_("Виберіть місто"),
        widget=forms.Select(
            attrs={"class": "form-select", "id": "start_point"},
        ),
    )
    end_point = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=_("Куди"),
        empty_label=_("Виберіть місто"),
        widget=forms.Select(
            attrs={"class": "form-select", "id": "end_point"},
        ),
    )
    date = forms.DateField(
        label=_("Дата поїздки"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control datepicker",
                "id": "date",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        id_value = kwargs.pop("id", None)
        start_point_value = kwargs.pop("start_point", None)
        end_point_value = kwargs.pop("end_point", None)
        date_value = kwargs.pop("date", None)

        # Call the super().__init__ method to initialize the form
        super(TripSearchForm, self).__init__(*args, **kwargs)

        # Set initial values for the fields based on the provided parameters
        self.fields["id"].initial = id_value
        self.fields["start_point"].initial = start_point_value
        self.fields["end_point"].initial = end_point_value
        self.fields["date"].initial = date_value
