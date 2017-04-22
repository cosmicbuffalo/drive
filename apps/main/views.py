# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *

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

    context = {
        "media_files": File.objects.all()


    }

    # if 'current_user' in request.session.keys():
    #     print "Current user success"

    #     context["folder"] =

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

def process_login(request):
    if request.method == "POST":

        print request.POST


    return redirect('/login')

def process_registration(request):
    if request.method == "POST":

        print request.POST

    return redirect("create_account_page")


# -----------------------
# - JSON RETURN METHODS -
# -----------------------

    # METHODS NECESSARY FOR LOGIN
def validate_identifier(request):
    if request.method == "POST":

        print request.POST['identifier']

        result = {}
        #Logic for this method will check to see if the posted identifier
        #exists in the database and what type it is, either phone or email.
        #If validation is successful, the returned data will include the
        #identifier type to be inserted into a hidden input and the identifier
        #to be displayed on the next screen.
        #successful result ->{'result':'success', 'messages':[messages], 'identifier_type':'email | phone', 'identifier':identifier}
        #failed result ->{'result':'failed_validation', 'messages':[messages]}
        return result

def authenticate_login(request):
    #separating login authentication from login processing for future ajax magic -
    #Authenticate login will resturn a JSON result to be handled by the success
    #function of the .ajax call which will then decide whether or not to call
    #process login to populate the session and redirect. The User manager class
    #will need to be updated for this too.
    if request.method == "POST":

        post_data = {
            'identifier_type':request.POST['identifier_type'], #obtained from hidden input on form
            'identifier':request.POST['identifier'],
            'password':request.POST['password']
        }

        #result = User.objects.authenticate_login(post_data)

        result = {}
        #Logic for this method will use the UserManager to authenticate the login.
        #If successful, the return result will pass only the user_id for handling
        #in the process login method.
        #successful result ->{'result':'success', 'messages':[messages], 'user_id':user_id}
        #failed result ->{'result':'failed_authentication', 'messages':[messages]}

        return result

# -----------------------
# - FILE UPLOAD METHOD -
# -----------------------
def file_upload(request):
    print 'yay'

    return redirect('home_root')








# CONTINUED....
