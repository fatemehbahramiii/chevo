import uuid
from django.conf import settings
from django.db import models

class Package(models.Model):
    name = models.CharField("نام پکیج", max_length=120)
    description = models.TextField("توضیحات", blank=True)
    price_rial = models.PositiveBigIntegerField("قیمت به ریال")
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ["price_rial"]
        verbose_name = "پکیج"
        verbose_name_plural = "پکیج‌ها"

    def __str__(self):
        return f"{self.name} — {self.price_rial:,} ریال"

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار پرداخت"
        PAID = "paid", "پرداخت‌شده"
        FAILED = "failed", "ناموفق"
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payments")
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name="payments")
    amount_rial = models.PositiveBigIntegerField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    provider = models.CharField(max_length=40, default="bitpay")
    provider_token = models.CharField(max_length=255, blank=True)
    provider_reference = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"{self.public_id} — {self.get_status_display()}"
