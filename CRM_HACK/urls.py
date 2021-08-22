"""CRM_HACK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth
from common.views import Index, SignUp, Dashboard, ProfileView, ProfileUpdate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile-update/', ProfileUpdate.as_view(), name='profile-update'),
    path('register/', SignUp.as_view(), name='register'),
    path('login/', auth.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(next_page='index'), name='logout'),
    path('change-password/', auth.PasswordChangeView.as_view(template_name='common/change-password.html', success_url='/'), name='change-password'),
    path('reset-password/', auth.PasswordResetView.as_view(template_name='common/reset-password/reset-password.html'), name='reset-password'),
    path('reset-password/done/', auth.PasswordResetDoneView.as_view(template_name='common/reset-password/reset-password-done.html'), name='reset-password-done'),
    path('reset-password/confirm/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(template_name='common/reset-password/reset-password-confirm.html'), name='reset-password-confirm'),
    path('reset-password/complete/', auth.PasswordResetCompleteView.as_view(template_name='common/reset-password/reset-password-complete.html'), name='reset-password-complete'),
    path('oauth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
