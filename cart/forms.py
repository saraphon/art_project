# cart/forms.py
from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'w-16 border px-2 py-1 rounded'}),
        }
