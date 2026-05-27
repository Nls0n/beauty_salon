from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["first_name", "specialty", "is_active"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя"}),
            "specialty": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: Топ-стилист"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
