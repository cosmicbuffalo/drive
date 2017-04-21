from django.conf.urls import url, include
from . import views

urlpatterns = [
    # TEMPLATE RENDERING ROUTES
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.show_login_page, name='login'),
    url(r'^create_account$', views.show_create_account_page, name="create_account_page"),
    url(r'^create_success$', views.show_create_success_page, name="create_success"),
    url(r'^home$', views.show_home_page_root, name="home_root"),
    url(r'^home/(?P<folder_id>\d+)$', views.show_home_page_folder, name="home_folder"),
    # REDIRECT ROUTES
    url(r'^process_login$', views.process_login, name="process_login"),
    url(r'^process_registration$', views.process_registration, name="process_registration")
]
