# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect


def index(request):
    return render(request, "main/index.html")


def show_login_page(request):

    if 'current_user' in request.session.keys():
        return redirect('/home')

    return render(request, 'main/login.html')

def show_create_account_page(request):

    if 'current_user' in request.session.keys():
        return redirect('/home')
    return HttpResponse("Create account page")

def process_login(request):
    if request.method == "POST":

        print request.POST['identifier']


    return redirect('/login')
