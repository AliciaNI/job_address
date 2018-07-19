from django.conf.urls import url
from . import views

handler404 = 'views.page_not_found'

urlpatterns = [
    url(r'^$', views.login, name='defalut'),
    url(r'^show/$', views.show, name='show'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^setting/$', views.setting, name='setting'),
    url(r'^map/$', views.map, name='map'),
    url(r'^createtable/$', views.createtable, name='createtable'),
    url(r'^search/$', views.search, name='search'),
    url(r'^tourldata/$', views.toUrlData, name='tourldata'),
]