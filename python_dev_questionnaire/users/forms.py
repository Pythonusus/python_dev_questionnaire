from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form.
    """

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Необязательное поле'}),
    )
    first_name = forms.CharField(
        required=False,
        label="Имя",
        widget=forms.TextInput(attrs={'placeholder': 'Необязательное поле'}),
    )
    last_name = forms.CharField(
        required=False,
        label="Фамилия",
        widget=forms.TextInput(attrs={'placeholder': 'Необязательное поле'}),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile that requires current password confirmation
    to commit changes.
    """

    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Необязательное поле'}),
        error_messages={
            'unique': 'Пользователь с таким email уже существует.'
        },
    )
    first_name = forms.CharField(
        required=False,
        label="Имя",
        widget=forms.TextInput(attrs={'placeholder': 'Необязательное поле'}),
    )
    last_name = forms.CharField(
        required=False,
        label="Фамилия",
        widget=forms.TextInput(attrs={'placeholder': 'Необязательное поле'}),
    )

    current_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput,
        help_text="Введите текущий пароль для подтверждения изменений.",
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        """
        Validate the username field to ensure uniqueness regardless of case.
        Using clean_username implementation from UserCreationForm.
        The only difference is that we exclude current instance from the query.
        """
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError(
                self.instance.unique_error_message(
                    self._meta.model, ["username"]
                )
            )
        return username

    def clean_current_password(self):
        """
        Validate that the current password is correct.
        """
        current_password = self.cleaned_data.get("current_password")
        if not self.instance.check_password(current_password):
            raise ValidationError(
                "Неверный пароль. Пожалуйста, введите правильный пароль."
            )
        return current_password
