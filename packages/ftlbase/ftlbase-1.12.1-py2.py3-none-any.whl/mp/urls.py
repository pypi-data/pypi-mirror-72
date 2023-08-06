from django.urls import path, include
from . import views

app_name = 'ftl-mp'

urlpatterns = [
    path('notifications/<str:reference>', views.NotificationView.as_view(), name='notifications'),
    path('post_payment/<str:reference>', views.PaymentSuccessView.as_view(), name='payment_success',),
    path('payment_failed/<str:reference>', views.PaymentFailedView.as_view(), name='payment_failure',),
    path('payment_pending/<str:reference>', views.PaymentPendingView.as_view(), name='payment_pending',),
]
