"""bodyfatcalculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

# bodyfatcalculator/urls.py
from django.contrib import admin
from django.urls import path, include
from calculator.views import home, page1, sleep_calculator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculator.urls')),
    path('sleep_calculator/', sleep_calculator, name='sleep_calculator'),
]
# bodyfatcalculator/urls.py



    
    # Add other URLs as needed

