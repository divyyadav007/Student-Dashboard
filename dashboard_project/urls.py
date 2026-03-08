"""
URL configuration for dashboard_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# admin provides Django's built-in admin site.
from django.contrib import admin

# include lets us plug another URL file into this project-level URL file.
from django.urls import include, path

# This list maps incoming URLs to the right handler.
urlpatterns = [
    # /admin/ opens the Django admin panel.
    path('admin/', admin.site.urls),
    # All app URLs from core.urls are mounted at the site root.
    path('', include('core.urls')),
]
