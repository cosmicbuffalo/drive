# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserManager(models.Manager):
    def login(self, postData):
        # print "running login function"

        failed_authentication = False
        messages = []

        try:
            found_user = User.objects.get(email=postData['email'])
        except:
            found_user = False
        #
        # print "found_user:"
        # print found_user

        if len(postData['email']) < 1:
            # print "Email is blank"
            messages.append("Email cannot be left blank!")
            failed_authentication = True
        elif not EMAIL_REGEX.match(postData['email']):
            # print "email doesn't match regex pattern"
            messages.append("Please enter a valid email!")
            failed_authentication = True
        elif not found_user:
            # print "found_user check came back false"
            messages.append("No user found with this email address. Please register new user.")
            failed_authentication = True

        if failed_authentication:
            # print "authentication failed before password check"
            return {'result':"failed_authentication", 'messages':messages}

        if len(postData['password']) < 8:
            # print "password is less than 8 characters"
            messages.append("Password must be at least 8 characters")
            return {'result':"failed_authentication", 'messages':messages}


        hashed_password = bcrypt.hashpw(str(postData['password']), str(found_user.salt))
        #
        # print "hashed password:"
        # print hashed_password
        #
        # print "found_user passoword:"
        # print found_user.password
        #

        if found_user.password != hashed_password:
            # print "found_user password doesn't match hashed password"
            messages.append("Incorrect password! Please try again")
            failed_authentication = True


        if failed_authentication:
            # print "authentication failed after password check"
            return {'result':"failed_authentication", 'messages':messages}
        else:
            # print "authentication succeeded, should be successfully logged in"
            messages.append('Successfully logged in!')
            return {'result':'success', 'messages':messages, 'user':found_user}

    def register(self, postData):
        # print "running register function"

        failed_validation = False
        messages = []

        if len(postData['first_name']) < 2:
            messages.append("First name must be at least 2 characters!")
            failed_validation = True
        elif not NAME_REGEX.match(postData['first_name']):
            messages.append("First name can only contain letters!")
            failed_validation = True

        if len(postData['last_name']) < 2:
            messages.append("Last name must be at least 2 characters!")
            failed_validation = True
        elif not NAME_REGEX.match(postData['last_name']):
            messages.append("Last name can only contain letters!")
            failed_validation = True
        try:
            found_user = User.objects.get(email=postData['email'])
        except:
            found_user = False

        if len(postData['email']) < 1:
            messages.append("Email is required!")
            failed_validation = True
        elif not EMAIL_REGEX.match(postData['email']):
            messages.append("Please enter a valid email!")
            failed_validation = True
        elif found_user:
            messages.append("This email is already registered!")
            failed_validation = True

        if len(postData['password']) < 1:
            messages.append("Password is required!")
            failed_validation = True
        elif len(postData['password']) < 8:
            messages.append("Password must be at least 8 characters")
            failed_validation = True
        elif postData['confirm_password'] != postData['password']:
            messages.append("Password confirmation failed")
            failed_validation = True

        if failed_validation:
            return {'result':"failed_validation", 'messages':messages}

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(str(postData['password']), str(salt))

        user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed_password, salt=salt)


        return {'result':"Successfully registered new user", 'messages':messages, 'user':user}

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Folder(models.Model):
    name = models.CharField(max_length=45)
    owner = models.ForeignKey(User, related_name="owned_folders")
    authorized_users = models.ManyToManyField(User, related_name="authorized_folders")
    parent_folder = models.ForeignKey('self', related_name="child_folders")
    is_in_trash = models.BooleanField(default=False)
    stars = models.ManyToManyField(User, related_name="starred_folders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#
# class Nest_relation(models.Model):
#     parent_folder = models.ForeignKey(Folder, related_name="parent_folder_relationships")
#     child_folder = models.ForeignKey(Folder, related_name="child_folder_relationship")

class File(models.Model):
    file_data = models.FileField() #need to figure out how this works
    file_type = models.CharField(max_length=15)
    owner = models.ForeignKey(User, related_name="owned_files")
    authorized_users = models.ManyToManyField(User, related_name="authorized_files")
    parent_folder = models.ForeignKey(Folder, related_name="child_files")
    is_in_trash = models.BooleanField(default=False)
    stars = models.ManyToManyField(User, related_name="starred_files")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# This class is for a potential bonus feature, tags, that I might implement later
#
# class Tag(models.Model):
#     title = models.CharField(max_length=45)
#     files = models.ManyToManyField(File, related_name="tags")
#     folders = models.ManyToManyField(Folder, related_name="tags")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
