# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

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

    context = {}

    if 'current_user' in request.session.keys():
        print "Current user success"

        context["folder"] = User.objects.get(pk=request.session.current_user).master_folder


    return render(request, "main/home.html", context)

def show_home_page_folder(request, folder_id):

    if 'current_user' in request.session.keys():
        print "Current user success"

    context = {
        "folder":Folder.objects.get(pk=folder_id)
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



# CONTINUED....
