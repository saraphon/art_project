from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded'}),
            'name': forms.TextInput(attrs={'class': 'w-full border px-3 py-2 rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full border px-3 py-2 rounded'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border px-3 py-2 rounded'}),
        }
