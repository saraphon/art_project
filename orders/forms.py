# orders/forms.py
from django import forms
from .models import ShippingAddress

BASE_INPUT_CLASS = "w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-500"

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "full_name", "phone",
            "address_line1", "address_line2",
            "city", "state", "postal_code", "country",
        ]
        # ป้ายกำกับภาษาไทย
        labels = {
            "full_name": "ชื่อ-นามสกุล",
            "phone": "เบอร์โทร",
            "address_line1": "ที่อยู่",
            "address_line2": "ที่อยู่",
            "city": "อำเภอ/เขต",
            "state": "จังหวัด",
            "postal_code": "รหัสไปรษณีย์",
            "country": "ประเทศ",
        }
        # ข้อความผิดพลาดภาษาไทย
        error_messages = {
            "full_name": {"required": "กรุณากรอกชื่อ-นามสกุล"},
            "phone": {"required": "กรุณากรอกเบอร์โทร"},
            "address_line1": {"required": "กรุณากรอกที่อยู่"},
            "city": {"required": "กรุณากรอกอำเภอ/เขต"},
            "state": {"required": "กรุณากรอกจังหวัด"},
            "postal_code": {"required": "กรุณากรอกรหัสไปรษณีย์"},
            "country": {"required": "กรุณากรอกประเทศ"},
        }
        # ใส่ placeholder + class สวย ๆ
        widgets = {
            "full_name":     forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
            "phone":         forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
            "address_line1": forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
            "address_line2": forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
            "city":          forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
            "state":         forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
            "postal_code":   forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
            "country":       forms.TextInput(attrs={"class": BASE_INPUT_CLASS, "placeholder": ""}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # กำหนดให้ country ค่าเริ่มต้นเป็น Thailand ถ้ายังว่าง
        if not self.initial.get("country"):
            self.initial["country"] = "Thailand"
