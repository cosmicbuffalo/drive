# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *
admin.site.register(User)
admin.site.register(Folder)
admin.site.register(Root_Folder)
admin.site.register(File)