from django.urls import path

from python_dev_questionnaire.users import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='users_register'),
    path(
        '<str:username>/',
        views.UserProfileView.as_view(),
        name='users_profile',
    ),
    path(
        '<str:username>/update/',
        views.UserUpdateView.as_view(),
        name='users_update',
    ),
    path(
        '<str:username>/update_password/',
        views.UserUpdatePasswordView.as_view(),
        name='users_update_password',
    ),
    path(
        '<str:username>/delete/',
        views.UserDeleteView.as_view(),
        name='users_delete',
    ),
]
