from django.conf.urls import url
from . import views

handler404 = 'views.page_not_found'

urlpatterns = [
    url(r'^analysis/$', views.analysis, name='analysis')
]