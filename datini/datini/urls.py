""" Datini URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import include, path
from django.views.generic import TemplateView

from tracker.views import AuthenticationForm, SignupView


def home(request):
    if request.user.is_authenticated:
        return redirect('expenses_list')
    else:
        return render(request, 'home.html')


urlpatterns = [
    path('', home, name='home'),
    path('expenses/', include('tracker.urls')),
    path('signup', SignupView.as_view(), name="signup"),
    path('login', LoginView.as_view(form_class=AuthenticationForm), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('info', TemplateView.as_view(template_name="info.html"), name="info")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
