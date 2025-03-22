from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpResponseNotFound,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.template import loader
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from python_dev_questionnaire.questions.models import Question

User = get_user_model()


@require_POST
def set_theme(request, theme):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie('django_theme', theme)
    return response


class IndexView(TemplateView):
    template_name = 'index.html'


class MaterialsView(ListView):
    template_name = 'materials.html'
    model = Question
    context_object_name = 'questions'


class AboutView(TemplateView):
    template_name = 'about.html'


class ProfileView(DetailView):
    template_name = 'profile.html'
    model = User
    context_object_name = 'user'


class LogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('index')
    success_message = 'Вы успешно вышли из системы'


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = 'Вы успешно вошли в систему'


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_message = 'Вы успешно зарегистрировались'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')


def error_404_view(request, exception=None, template_name='errors/404.html'):
    """404 handler"""
    context = {
        'error_message': 'The page you are looking for does not exist.',
    }
    return HttpResponseNotFound(
        loader.render_to_string(
            template_name, context, request=request, using=None
        )
    )


def error_500_view(request, template_name='errors/500.html'):
    """500 handler"""
    context = {
        'error_message': 'An internal server error occurred.',
    }
    return HttpResponseServerError(
        loader.render_to_string(
            template_name, context, request=request, using=None
        )
    )
