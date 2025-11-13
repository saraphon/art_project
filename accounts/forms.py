from django import forms
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Address

# ✅ ฟอร์มสำหรับ Login (Allauth)
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'border border-gray-300 rounded px-3 py-2 w-full',
            'placeholder': 'Username or Email',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'border border-gray-300 rounded px-3 py-2 w-full',
            'placeholder': 'Password',
        })


# ✅ ฟอร์มสำหรับแก้ไขโปรไฟล์
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='ชื่อ', required=False)
    phone = forms.CharField(label='เบอร์โทรศัพท์', required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
        self.fields['phone'].initial = self.instance.phone  # ✅ ใช้ phone

    def save(self, commit=True):
        profile = super().save(commit=False)

        # อัปเดตชื่อใน user
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            if commit:
                self.user.save()

        # อัปเดตเบอร์โทรใน Profile
        profile.phone = self.cleaned_data['phone']

        if commit:
            profile.save()

        return profile


# ✅ ฟอร์มสำหรับสมัครสมาชิก (Allauth)
class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=150, label="ชื่อ", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ชื่อฟิลด์เป็นไทย
        self.fields["email"].label = "อีเมล"
        self.fields["username"].label = "ชื่อผู้ใช้"
        self.fields["password1"].label = "รหัสผ่าน"
        self.fields["password2"].label = "ยืนยันรหัสผ่าน"

        # ซ่อน help_text ของรหัสผ่าน (ที่เป็นอังกฤษยาว ๆ)
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        # ใส่คลาส/placeholder ให้ดูเป็นไทย
        base_classes = "w-full px-4 py-2 border rounded bg-white focus:outline-none focus:ring"
        placeholders = {
            "email": "อีเมล",
            "username": "ชื่อผู้ใช้",
            "full_name": "ชื่อ",
            "password1": "รหัสผ่าน",
            "password2": "ยืนยันรหัสผ่าน",
        }
        for name, field in self.fields.items():
            widget = field.widget
            if getattr(widget, "input_type", "") != "checkbox":
                widget.attrs["class"] = (widget.attrs.get("class", "") + " " + base_classes).strip()
            if name in placeholders:
                widget.attrs.setdefault("placeholder", placeholders[name])

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("full_name", "")
        user.save()
        Profile.objects.update_or_create(user=user, defaults={})
        return user

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_line',
            'sub_district',  # ตำบล/แขวง
            'district',      # อำเภอ/เขต
            'province',      # จังหวัด
            'postal_code',   # รหัสไปรษณีย์
            'country'        # ประเทศ
        ]
        widgets = {
            'address_line': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_district': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }