from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.show_login_page, name='login'),
    url(r'^process_login$', views.process_login, name="process_login"),
    url(r'^create_account$', views.show_create_account_page, name="create_account_page")
]
