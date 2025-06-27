from django.urls import path

from apps.users.api_endpoints.auth.forget_password.confirm_otp.views import ForgotPasswordConfirmOTPAPIView
from apps.users.api_endpoints.auth.forget_password.finalizer.views import ForgotPasswordFinalizerAPIView
from apps.users.api_endpoints.auth.forget_password.send_otp.views import ForgotPasswordSendOTPAPIView
from apps.users.api_endpoints.auth.register.confirm_otp.views import RegistrationConfirmOTPAPIView
from apps.users.api_endpoints.auth.register.finalizer.views import RegistrationFinalizerAPIView
from apps.users.api_endpoints.auth.register.send_otp.views import RegistrationSendOTPAPIView
from apps.users.api_endpoints.list.views import UserSearchAPIView
from apps.users.api_endpoints.profile.delete_profile.views import UserDestroyAPIView
from apps.users.api_endpoints.profile.profile.views import UserModelAPIView

app_name = "apps.users"

urlpatterns = [
	path('registration/send-otp/', RegistrationSendOTPAPIView.as_view(), name='registration_send_otp'),
	path('registration/confirm-otp/', RegistrationConfirmOTPAPIView.as_view(), name='registration_confirm_otp'),
	path('registration/finalizer/', RegistrationFinalizerAPIView.as_view(), name='registration_finalize'),
	path('forgot-password/send-otp/', ForgotPasswordSendOTPAPIView.as_view(), name='forgot_password_send_otp'),
	path('forgot-password/confirm-otp/', ForgotPasswordConfirmOTPAPIView.as_view(), name='forgot_password_confirm_otp'),
	path('forgot-password/finalizer/', ForgotPasswordFinalizerAPIView.as_view(), name='forgot_password_finalize'),
	path('profile/delete/', UserDestroyAPIView.as_view(), name='delete_account'),
	path('profile/', UserModelAPIView.as_view(), name='profile'),
	path('users/search/', UserSearchAPIView.as_view(), name='user-search')
]
