import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Package, Payment

def package_list(request):
    return render(request, "payments/packages.html", {"packages": Package.objects.filter(is_active=True)})

@login_required
def start_payment(request, package_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    package = get_object_or_404(Package, pk=package_id, is_active=True)
    payment = Payment.objects.create(user=request.user, package=package, amount_rial=package.price_rial)
    api_key = getattr(settings, "BITPAY_API_KEY", "")
    endpoint = getattr(settings, "BITPAY_CREATE_PAYMENT_URL", "")
    if not api_key or not endpoint:
        messages.error(request, "درگاه هنوز پیکربندی نشده است؛ تنظیمات رسمی API را وارد کنید.")
        payment.status = Payment.Status.FAILED
        payment.save(update_fields=["status"])
        return redirect("payments:packages")
    # Match payload/response fields to the official merchant API documentation before production.
    payload = {"api": api_key, "amount": payment.amount_rial,
               "redirect": getattr(settings, "BITPAY_CALLBACK_URL", ""),
               "factorId": str(payment.public_id), "name": request.user.get_username(),
               "email": request.user.email}
    try:
        response = requests.post(endpoint, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        token = str(data.get("token", data.get("id", "")))
        redirect_base = getattr(settings, "BITPAY_REDIRECT_BASE_URL", "")
        if not token or not redirect_base:
            raise ValueError("Missing token or redirect URL in configuration")
        payment.provider_token = token
        payment.save(update_fields=["provider_token"])
        return redirect(f"{redirect_base.rstrip('/')}/{token}")
    except (requests.RequestException, ValueError):
        payment.status = Payment.Status.FAILED
        payment.save(update_fields=["status"])
        messages.error(request, "ارتباط با درگاه برقرار نشد؛ تنظیمات API را بررسی کنید.")
        return redirect("payments:packages")

@csrf_exempt
def payment_callback(request):
    # Do not mark a payment as paid based only on a browser redirect.
    # Implement server-to-server verification using the provider's official API.
    token = request.GET.get("token") or request.POST.get("token")
    if not token:
        return HttpResponseBadRequest("Missing payment token")
    payment = Payment.objects.filter(provider_token=token).first()
    if payment is None:
        return HttpResponseBadRequest("Unknown payment")
    return render(request, "payments/callback_pending.html", {"payment": payment})