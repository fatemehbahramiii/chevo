import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Package",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="نام پکیج")),
                ("description", models.TextField(blank=True, verbose_name="توضیحات")),
                ("price_rial", models.PositiveBigIntegerField(verbose_name="قیمت به ریال")),
                ("is_active", models.BooleanField(default=True, verbose_name="فعال")),
            ],
            options={"verbose_name": "پکیج", "verbose_name_plural": "پکیج‌ها", "ordering": ["price_rial"]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("public_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("amount_rial", models.PositiveBigIntegerField()),
                ("status", models.CharField(choices=[("pending", "در انتظار پرداخت"), ("paid", "پرداخت‌شده"), ("failed", "ناموفق")], default="pending", max_length=12)),
                ("provider", models.CharField(default="bitpay", max_length=40)),
                ("provider_token", models.CharField(blank=True, max_length=255)),
                ("provider_reference", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("package", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="payments", to="payments.package")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="payments", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "پرداخت", "verbose_name_plural": "پرداخت‌ها", "ordering": ["-created_at"]},
        ),
    ]
