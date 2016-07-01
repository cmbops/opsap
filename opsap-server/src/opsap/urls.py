"""opsap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-token-auth/', views.ObtainExAuthToken.as_view()),
    url(r'^param/', include([
        url(r'^set/$', views.param_set),
        url(r'^get/$', views.param_get),
    ])),
    url(r'^options/', include([
        url(r'^add/$', views.option_add),
        url(r'^list/$', views.option_list),
        url(r'^edit/$', views.option_edit),
        url(r'^delete/$', views.option_delete),
    ])),
    url(r'^ouser/', include('ouser.urls')),
    # url(r'^odata/', include('odata.urls')),
    # url(r'^ovm/', include('ovm.urls')),
]
