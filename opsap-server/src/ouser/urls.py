from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^user/', include([
        url(r'^add/$', views.user_add),
        url(r'^list/$', views.user_list),
        url(r'^detail/$', views.user_detail),
        url(r'^edit/$', views.user_edit),
        url(r'^delete/$', views.user_delete),
    ])),
    url(r'^group/', include([
        url(r'^add/$', views.group_add),
        url(r'^list/$', views.group_list),
        url(r'^edit/$', views.group_edit),
        url(r'^delete/$', views.group_delete),
    ])),
]
