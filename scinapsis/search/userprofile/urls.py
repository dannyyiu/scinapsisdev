from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.index, name='profilepage'),
    url(r'^profile/update/$', views.update_profile, name='update_profile'),
]