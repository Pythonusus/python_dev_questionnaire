from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
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
from django.views.generic import ListView, TemplateView

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


class CustomLogoutView(LogoutView):
    """
    Logout user using Django's built-in logout view.
    Redirects to the login page after successful logout.
    Shows a success message after successful logout.
    """
    next_page = reverse_lazy('login')
    success_message = 'Вы успешно вышли из системы'

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch the logout view.
        Shows a success message after successful logout.
        Can't use SuccessMessageMixin here because it doesn't
        work with LogoutView.
        """
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response


class CustomLoginView(SuccessMessageMixin, LoginView):
    """
    Login user using Django's built-in login view.
    Redirects to the index page after successful login.
    Shows a success message after successful login.
    """
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_message = 'Вы успешно вошли в систему'
    next_page = reverse_lazy('index')


def error_404_view(request, exception=None, template_name='errors/404.html'):
    """Custom 404 errorhandler"""
    context = {
        'error_message': (
            'Вы сказали своим друзьям, что не будете брать с собой телефон, '
            'чтобы попробовать путешествовать как в старые времена. '
            'Вы купили карту и бутылку воды и взяли с собой камеру '
            'для фотографий. Но карта была из 2005 года, '
            'и ландшафт изменился. Так что вы здесь, в середине пустого поля, '
            'которое карта продолжает считать нужной вам страницей.'
        )
    }
    return HttpResponseNotFound(
        loader.render_to_string(
            template_name, context, request=request, using=None
        )
    )


def error_500_view(request, template_name='errors/500.html'):
    """Custom 500 error handler"""
    context = {
        'error_message': (
            'Собака украла провод от сервера. Мы уже знаем о проблеме и '
            'работаем над ее решением. Пожалуйста подождите пока мы '
            'ловим собаку.'
        )
    }
    return HttpResponseServerError(
        loader.render_to_string(
            template_name, context, request=request, using=None
        )
    )
