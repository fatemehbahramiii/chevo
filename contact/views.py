from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import ContactForm, RegisterForm

@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        item = form.save()
        try:
            send_mail(
                subject=f"[CHEVO] {item.subject}",
                message=f"نام: {item.name}\nایمیل: {item.email}\n\n{item.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "پیام شما ثبت شد. با شما تماس می‌گیریم.")
        except Exception:
            # The message is safely saved in the database/admin even if email delivery is not configured.
            messages.warning(request, "پیام ثبت شد، اما ارسال ایمیل انجام نشد. لطفاً تنظیمات ایمیل را بررسی کنید.")
        return redirect(request.META.get("HTTP_REFERER") or "home")
    messages.error(request, "اطلاعات فرم معتبر نیست؛ لطفاً فیلدها را بررسی کنید.")
    return redirect(request.META.get("HTTP_REFERER") or "home")

def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "حساب کاربری شما ساخته شد.")
        return redirect("accounts:dashboard")
    return render(request, "accounts/register.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")
