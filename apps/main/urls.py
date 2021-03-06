from django.conf.urls import url, include
from . import views

urlpatterns = [
    # TEMPLATE RENDERING ROUTES
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.show_login_page, name='login'),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^create_account$', views.show_create_account_page, name="create_account_page"),
    url(r'^create_success$', views.show_create_success_page, name="create_success"),
    url(r'^home$', views.show_home_page_root, name="home_root"),
    url(r'^home/(?P<folder_id>\d+)$', views.show_home_page_folder, name="home_folder"),
    url(r'^home_body$', views.render_root_folder_contents, name="get_home_contents"),
    url(r'^home/folder_body/(?P<folder_id>\d+)$', views.render_contents_of_folder, name="get_folder_contents"),
    url(r'^home/trash$',views.render_trash_contents, name="get_trash_contents"),
    url(r'^home/shared$', views.render_shared_with_me, name="get_shared_contents"),
    url(r'^right_click$', views.render_right_click_menu, name="get_right_click_menu"),
    # REDIRECT ROUTES
    url(r'^process_login$', views.process_login, name="process_login"),
    url(r'^process_registration$', views.process_registration, name="process_registration"),
    url(r'^folder_creation/(?P<folder_id>\d+)$', views.folder_creation, name='folder_creation'),
    # JSON ROUTES
    url(r'^validate_identifier$', views.validate_identifier, name="validate_identifier"),
    url(r'^authenticate_login$', views.authenticate_login, name="authenticate_login"),
    url(r'^validate_registration$', views.validate_registration, name="validate_registration"),
    url(r'^share_items/(?P<folder_id>\d+)$', views.share_items_by_emails, name="share_items"),
    url(r'^recent_uploads', views.recent_uploads, name="recent_uploads"),

    #FILE MANIPULATION ROUTES (JSON)
    url(r'^move_to_trash$', views.move_to_trash, name="move_to_trash"),
    url(r'^toggle', views.grid_view, name="grid_view"),
    # Test Route for File upload
    url(r'^file_upload/(?P<folder_id>\d+)$', views.file_upload, name='file_upload'),
    # Going into a folder




]
