from django.db import models

class ContactMessage(models.Model):
    name = models.CharField("نام", max_length=120)
    email = models.EmailField("ایمیل")
    subject = models.CharField("موضوع", max_length=180)
    message = models.TextField("پیام")
    created_at = models.DateTimeField("زمان ارسال", auto_now_add=True)
    is_read = models.BooleanField("خوانده شده", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f"{self.name} — {self.subject}"
