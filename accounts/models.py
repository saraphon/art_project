from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    sub_district = models.CharField(max_length=100, default='ไม่ระบุ')
    district = models.CharField(max_length=100, default='ไม่ระบุ')
    province = models.CharField(max_length=100, default='ไม่ระบุ')  # ✅ เพิ่ม default
    postal_code = models.CharField(max_length=10, default='00000')    # ✅ เพิ่ม default
    country = models.CharField(max_length=100, default="Thailand")

    def __str__(self):
        return f"{self.address_line} ({self.user.username})"
