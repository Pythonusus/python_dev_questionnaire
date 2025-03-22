from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from python_dev_questionnaire.custom_mixins import OwnershipRequiredMixin
from python_dev_questionnaire.users.forms import (
    CustomUserCreationForm,
    UserUpdateForm,
)

User = get_user_model()


class UserProfileView(LoginRequiredMixin, OwnershipRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    model = User
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    login_url = reverse_lazy('login')

    # OwnershipRequiredMixin settings
    ownership_field = 'user'
    permission_denied_message = (
        'Можно просматривать только свой профиль. '
        'Если это тоже ваш аккаунт, войдите в него чтобы просматривать.'
    )
    permission_denied_redirect_url = 'login'


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Register user using Django's built-in register view.
    Redirects to the login page after successful registration.
    Shows a success message after successful registration.
    """

    model = User
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_message = 'Вы успешно зарегистрировались'
    success_url = reverse_lazy('login')


class UserUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, OwnershipRequiredMixin, UpdateView
):
    """
    Update user. Users cannot update other users.
    Redirects to the profile page after successful update if username
    wasn't changed.
    Redirects to the login page if username was changed. Will require re-login.
    Shows a success message after successful update.
    """

    model = User
    template_name = 'users/update.html'
    form_class = UserUpdateForm
    slug_field = 'username'
    slug_url_kwarg = 'username'
    login_url = reverse_lazy('login')

    # OwnershipRequiredMixin settings
    ownership_field = 'user'
    permission_denied_message = (
        'Вы не можете обновить профиль другого пользователя. '
        'Если это тоже ваш аккаунт, войдите в него чтобы обновить.'
    )
    permission_denied_redirect_url = 'login'

    success_message = 'Профиль успешно обновлен'

    def get_success_url(self):
        return reverse_lazy(
            'users_profile', kwargs={'username': self.request.user.username}
        )


class UserUpdatePasswordView(
    SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView
):
    """
    Update user password using Django's built-in PasswordChangeView.
    Requires user to be logged in.
    Redirects to the profile page after successful password change.
    Shows a success message after successful password change.
    """

    template_name = 'users/password_update.html'
    success_message = 'Пароль успешно изменен'

    def get_success_url(self):
        return reverse_lazy(
            'users_profile', kwargs={'username': self.request.user.username}
        )


class UserDeleteView(
    SuccessMessageMixin, LoginRequiredMixin, OwnershipRequiredMixin, DeleteView
):
    """
    Delete user. Users cannot delete other users.
    Redirects to the registration page after successful deletion.
    Shows a success message after successful deletion.
    """

    model = User
    template_name = 'users/delete.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    login_url = reverse_lazy('login')

    # OwnershipRequiredMixin settings
    ownership_field = 'user'
    permission_denied_message = (
        'Вы не можете удалить профиль другого пользователя. '
        'Если это тоже ваш аккаунт, войдите в него чтобы удалить.'
    )
    permission_denied_redirect_url = 'login'

    success_message = 'Профиль успешно удален'
    success_url = reverse_lazy('users_register')
