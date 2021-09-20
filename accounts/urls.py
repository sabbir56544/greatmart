from django.urls import path
from .views import sign_up_view, log_in, ActivateAccount, waiting


urlpatterns = [
    path('register/', sign_up_view, name='register'),
    path('login/', log_in, name='login'),
    path('activate/mail', waiting, name='waiting'),
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='activate'),
]    