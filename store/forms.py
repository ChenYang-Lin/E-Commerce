from django import forms
from django.forms import widgets
from .models import Customer, Product


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email']

        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
