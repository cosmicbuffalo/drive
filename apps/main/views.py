# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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



    context = {
        "user": User.objects.get(id=request.session['current_user']),
        "media_files": File.objects.all().order_by("-created_at"),
        "file_form" : file_form,
        'folder_form': folder_form

    }

    # if 'current_user' in request.session.keys():
    #     print "Current user success"

    #     context["folder"] =
    print request.session

    return render(request, "main/home.html", context)

def show_home_page_folder(request, folder_id):

    if 'current_user' in request.session.keys():
        print "Current user success"

    context = {
        "folder":Folder.objects.get(pk=folder_id)
    }
    media = {

    }

    return render(request, "main/home.html", context)

# ------------------------------
# - LOGIN/REGISTRATION METHODS -
# ------------------------------

def logout(request):
    request.session.clear()
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





# -----------------------
# - FILE UPLOAD METHOD -
# -----------------------
def file_upload(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        user = User.objects.get(id=request.session['current_user'])
        File.objects.create(file_data=request.FILES.get('file_data'),file_type='image', owner=user)
        uploaded_file = File.objects.filter(owner_id=request.session['current_user']).order_by('-created_at')[0]

        file_info = {
            'file_data':uploaded_file.file_data,
            'owner_name':uploaded_file.owner.first_name,
            'updated_at':uploaded_file.updated_at,
            'file_size':uploaded_file.file_data.size|filesizeformat
        }


    return JsonResponse(file_info)



def folder_creation(request):
    if request.method == "POST":
        form = FolderForm(request.POST)

    return redirect('home_root')








# CONTINUED....
