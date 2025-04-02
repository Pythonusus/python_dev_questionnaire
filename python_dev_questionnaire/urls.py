"""
URL configuration for python_dev_questionnaire project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from python_dev_questionnaire import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    debug_urlpatterns = []

    # Debug toolbar URLs
    import debug_toolbar
    debug_urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    # Browser reload URLs
    debug_urlpatterns += [
        path("__reload__/",
        include("django_browser_reload.urls")
        )
    ]

    # Add all debug URLs to the main urlpatterns
    urlpatterns = urlpatterns + debug_urlpatterns
