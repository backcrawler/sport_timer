"""sport_timer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('adminenter/', admin.site.urls),
    path('', include('timing.urls', namespace='timing')),
    path('accounts', include('users.urls', namespace='users'))
]


# def get_success_url(self):
#     """Return the URL to redirect to after processing a valid form."""
#     if self.success_url:
#         url = self.success_url.format(**self.object.__dict__)
# self.object = form.save()