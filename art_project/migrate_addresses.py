from django.apps import apps
from orders.models import ShippingAddress
from django.db import transaction


def migrate_accounts_address_to_shipping():
    Address = apps.get_model('accounts', 'Address')

    def pick(obj, *names, default=""):
        for n in names:
            if hasattr(obj, n):
                v = getattr(obj, n)
                if v:
                    return v
        return default

    migrated = 0
    skipped = 0

    with transaction.atomic():
        for a in Address.objects.select_related('user').all():
            user = getattr(a, "user", None)
            if not user:
                skipped += 1
                continue

            # map ฟิลด์จาก accounts.Address -> orders.ShippingAddress
            full_name   = user.get_full_name() or user.username
            phone       = ""  # โมเดลเดิมไม่มี
            line1       = pick(a, "address_line", default="")
            line2       = pick(a, "sub_district", default="")
            city        = pick(a, "district", default="")
            state       = pick(a, "province", default="")
            postal_code = pick(a, "postal_code", default="")
            country     = pick(a, "country", default="Thailand")

            sa, created = ShippingAddress.objects.get_or_create(
                user=user,
                full_name=full_name,
                phone=phone,
                address_line1=line1,
                address_line2=line2,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
            )
            if created:
                migrated += 1
            else:
                skipped += 1

    return migrated, skipped
