# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import glob
from django.shortcuts import render, redirect, reverse
from .models import *
from forms import *
from django.http import HttpResponseRedirect, JsonResponse

# --------------------------
# - HTML RENDERING METHODS -
# --------------------------

def index(request):
    return render(request, "main/index.html")

def show_login_page(request):

    if 'current_user' in request.session.keys():
        return redirect('/home')

    return render(request, 'main/login.html')

def show_create_account_page(request):

    if 'current_user' in request.session.keys():
        return redirect('/home')
    return render(request, "main/create_account.html")

def show_create_success_page(request):

    if 'current_user' in request.session.keys():
        print "Current user success"
    return render(request, "main/create_success.html")


def show_home_page_root(request):
    file_form = FileForm()
    folder_form = FolderForm()
    if 'current_user' in request.session.keys():
        print "Current user in session: ---->", request.session['current_user']
    else:
        return redirect('login')

    parent_folder = Root_Folder.objects.get(user_id=request.session['current_user']).folder


    context = {
        "user": User.objects.get(id=request.session['current_user']),
        "media_files": File.objects.filter(parent_folder=parent_folder).exclude(is_in_trash=True).order_by('-created_at'),
        'folders': Folder.objects.filter(parent_folder=parent_folder).exclude(is_in_trash=True).order_by('-created_at'),
        "file_form" : file_form,
        'folder_form': folder_form,
        "parent_folder" : parent_folder,

    }

    # if 'current_user' in request.session.keys():
    #     print "Current user success"

    #     context["folder"] =
    print request.session

    return render(request, "main/home.html", context)

def render_root_folder_contents(request):

    parent_folder = Root_Folder.objects.get(user_id=request.session['current_user']).folder

    context = {
        'media_files':File.objects.filter(parent_folder=parent_folder).exclude(is_in_trash=True).order_by('-created_at'),
        'folders': Folder.objects.filter(parent_folder=parent_folder).exclude(is_in_trash=True).order_by('-created_at'),
    }

    return render(request, 'main/table_body_partial.html', context)

def render_contents_of_folder(request, folder_id):

    context = {
        'media_files':File.objects.filter(parent_folder__id=folder_id).exclude(is_in_trash=True).order_by('-created_at'),
        'folders':Folder.objects.filter(parent_folder__id=folder_id).exclude(is_in_trash=True).order_by('-created_at')
    }
    return render(request, 'main/table_body_partial.html', context)






def show_home_page_folder(request, folder_id):

    file_form = FileForm()
    folder_form = FolderForm()

    folder = Folder.objects.get(id=folder_id)
    # folder2 = Folder.objects.filter(parent_folder=folder).order_by('-created_at')


    context = {
        "user": User.objects.get(id=request.session['current_user']),
        "media_files": File.objects.filter(parent_folder=folder).order_by('-created_at'),
        "folders": Folder.objects.filter(parent_folder=folder).order_by('-created_at'),
        'parent_folder' : folder,
        "file_form" : file_form,
        'folder_form': folder_form,


    }

    return render(request, "main/home.html", context)

# ------------------------------
# - LOGIN/REGISTRATION METHODS -
# ------------------------------

def logout(request):
    request.session.clear()

    if request.method == "POST":
        return JsonResponse({'redirect':True, 'redirect_url':'/login'})

    return redirect('login')

def process_login(request):
    if request.method == "POST":

        print "Entered process_login method"

        print "request.POST: --------> ", request.POST
        print "current user: -------->", request.POST['user_id']

        request.session['current_user'] = request.POST['user_id']


    return redirect('/home')

def process_registration(request):
    if request.method == "POST":
        print "Entered process_registration method in views.py"
        print "request.POST ---------->", request.POST

        for key in request.POST.keys():
            print "key: --->", key
            print "value: ----------->", request.POST[key]
        try:
            result = User.objects.register_user(request.POST)
            print result
        except:
            print "something went wrong, failed to create user"
            return JsonResponse({'result':'ERROR'})

        if result['result'] == "ERROR":
            print "register_user returned error result"
            return JsonResponse({'result':'ERROR'})

        request.session['current_user'] = result['user'].id

        print "creating new root folder for registered user"
        new_user_root_folder = Folder.objects.create(
                                                        name="{}_root".format(result['user'].id),
                                                        owner=result['user'],
                                                        is_master_folder=True
                                                    )
        print "assigning Root_Folder relationship for new root folder of registered user"
        Root_Folder.objects.create(user=result['user'], folder=new_user_root_folder)

        print "success"
        print "current_user in session:",  request.session['current_user']

    return JsonResponse({'redirect':True,'redirect_url':'/home'})


# -----------------------
# - JSON RETURN METHODS -
# -----------------------

    # METHODS NECESSARY FOR LOGIN
def validate_identifier(request):
    if request.method == "POST":


        print "Recieved identifier ----->", request.POST['identifier']

        result = User.objects.validate_identifier(request.POST['identifier'])
        print result
        #Logic for this method will check to see if the posted identifier
        #exists in the database and what type it is, either phone or email.
        #If validation is successful, the returned data will include the
        #identifier type to be inserted into a hidden input and the identifier
        #to be displayed on the next screen.
        #successful result ->{'result':'success', 'messages':[messages], 'identifier_type':'email | phone', 'identifier':identifier}
        #failed result ->{'result':'failed_validation', 'messages':[messages]}
        return JsonResponse(result)

def authenticate_login(request):
    #separating login authentication from login processing for future ajax magic -
    #Authenticate login will resturn a JSON result to be handled by the success
    #function of the .ajax call which will then decide whether or not to call
    #process login to populate the session and redirect. The User manager class
    #will need to be updated for this too.
    print "running authenticate_login in views.py"
    if request.method == "POST":

        print "request.POST: ---->", request.POST

        #result = User.objects.authenticate_login(post_data)

        result = User.objects.authenticate_login(request.POST)
        #Logic for this method will use the UserManager to authenticate the login.
        #If successful, the return result will pass only the user_id for handling
        #in the process login method.
        #successful result ->{'result':'success', 'messages':[messages], 'user_id':user_id}
        #failed result ->{'result':'failed_authentication', 'messages':[messages]}

        return JsonResponse(result)



# Methods necessary for registration

def validate_registration(request):

    print "Running validate_registration in views.py"

    if request.method == "POST":

        print "request.POST: ---->", request.POST

        result = User.objects.validate_registration(request.POST)


        return JsonResponse(result)



# -----------------------------
# - FILE MANIPULATION METHODS -
# -----------------------------

def move_selected_to_trash(request, list_of_selected):

    for selected_item in list_of_selected:
        print selected_item


    return JsonResponse({'redirect':True, 'redirect_url':'/home'})



# -----------------------
# - FILE UPLOAD METHOD -
# -----------------------
def file_upload(request, folder_id):
    print "didnt run method"
    if request.method == "POST":
        print"Fired"
        form = FileForm(request.POST, request.FILES)
        file_name = request.FILES['file_data'].name
        if ".txt" in file_name:
            file_type = "text"
        if ".png" in file_name:
            file_type = "image"
        if ".img" in file_name:
            file_type = "image"

        if '.jpg' in file_name:
            file_type = "image"

        if '.gif' in file_name:
            file_type = "image"

        if ".mp4" in file_name:
            file_type = "video"

        folder = Folder.objects.get(id=folder_id)
        user = User.objects.get(id=request.session['current_user'])

        File.objects.create(file_data=request.FILES.get('file_data'),file_type=file_type, owner=user, parent_folder=folder)


        # uploaded_file = File.objects.filter(owner_id=request.session['current_user']).order_by('-created_at')[0]

        # file_info = {
        #     'file_data':uploaded_file.file_data,
        #     'owner_name':uploaded_file.owner.first_name,
        #     'updated_at':uploaded_file.updated_at,
        #     'file_size':uploaded_file.file_data.size|filesizeformat
        # }
    # return JsonResponse(file_info)

    return redirect(reverse("home_folder", kwargs={'folder_id':folder_id}))

def folder_creation(request, folder_id):
    if request.method == "POST":
        user = User.objects.get(id= request.session['current_user'])

        parent_folder = Folder.objects.get(id=folder_id)

        parent_folder.child_folders.add(Folder.objects.create(name=request.POST.get('name'), owner=user))

        # Folder.objects.create(name=request.POST.get('name'), owner=user, parent_folder=parent_folder)
    return redirect(reverse("home_folder", kwargs={'folder_id':folder_id}))






# CONTINUED....
