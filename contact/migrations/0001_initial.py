from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="نام")),
                ("email", models.EmailField(max_length=254, verbose_name="ایمیل")),
                ("subject", models.CharField(max_length=180, verbose_name="موضوع")),
                ("message", models.TextField(verbose_name="پیام")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="زمان ارسال")),
                ("is_read", models.BooleanField(default=False, verbose_name="خوانده شده")),
            ],
            options={"verbose_name": "پیام تماس", "verbose_name_plural": "پیام‌های تماس", "ordering": ["-created_at"]},
        ),
    ]
