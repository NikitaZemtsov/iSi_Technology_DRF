"""iSi_Technology_DRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from chat.views import ThreadApiView, UserThread, UserMsg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/threads/', UserThread.as_view(), name='threads'),
    path('api/v1/threads/<int:thread_id>/', ThreadApiView.as_view(), name='thread'),
    path('api/v1/threads/<int:thread_id>/msgs/', ThreadApiView.as_view(), name='thread_msgs'),
    path('api/v1/msgs/', UserMsg.as_view(), name='msgs'),
]
