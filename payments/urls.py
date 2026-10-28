from django.urls import path
from . import views
app_name = "payments"
urlpatterns = [
    path("packages/", views.package_list, name="packages"),
    path("start/<int:package_id>/", views.start_payment, name="start"),
    path("callback/", views.payment_callback, name="callback"),
]