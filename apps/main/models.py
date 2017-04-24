# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import time
from django.db import models
from django.core.validators import RegexValidator
import re, bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')


class UserManager(models.Manager):
    # def login(self, postData):
    #     # print "running login function"
    #
    #     failed_authentication = False
    #     messages = []
    #
    #     try:
    #         found_user = User.objects.get(email=postData['email'])
    #     except:
    #         found_user = False
    #     #
    #     # print "found_user:"
    #     # print found_user
    #
    #     if len(postData['email']) < 1:
    #         # print "Email is blank"
    #         messages.append("Email cannot be left blank!")
    #         failed_authentication = True
    #     elif not EMAIL_REGEX.match(postData['email']):
    #         # print "email doesn't match regex pattern"
    #         messages.append("Please enter a valid email!")
    #         failed_authentication = True
    #     elif not found_user:
    #         # print "found_user check came back false"
    #         messages.append("No user found with this email address. Please register new user.")
    #         failed_authentication = True
    #
    #     if failed_authentication:
    #         # print "authentication failed before password check"
    #         return {'result':"failed_authentication", 'messages':messages}
    #
    #     if len(postData['password']) < 8:
    #         # print "password is less than 8 characters"
    #         messages.append("Password must be at least 8 characters")
    #         return {'result':"failed_authentication", 'messages':messages}
    #
    #
    #     hashed_password = bcrypt.hashpw(str(postData['password']), str(found_user.salt))
    #     #
    #     # print "hashed password:"
    #     # print hashed_password
    #     #
    #     # print "found_user passoword:"
    #     # print found_user.password
    #     #
    #
    #     if found_user.password != hashed_password:
    #         # print "found_user password doesn't match hashed password"
    #         messages.append("Incorrect password! Please try again")
    #         failed_authentication = True
    #
    #
    #     if failed_authentication:
    #         # print "authentication failed after password check"
    #         return {'result':"failed_authentication", 'messages':messages}
    #     else:
    #         # print "authentication succeeded, should be successfully logged in"
    #         messages.append('Successfully logged in!')
    #         return {'result':'success', 'messages':messages, 'user':found_user}

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


    def validate_registration(self, postData):

        failed_validation = False
        messages = {
            'name_errors':[],
            'email_errors':[],
            'password_errors':[],
            'password_confirm_errors':[],
            'birthday_errors':[],
            'gender_errors':[],
            'phone_errors':[],
            'location_errors':[]
        }

        if len(postData['first_name']) < 2:
            messages['name_errors'].append("First name must be at least 2 characters!")
            failed_validation = True
        elif not NAME_REGEX.match(postData['first_name']):
            messages['name_errors'].append("First name can only contain letters!")
            failed_validation = True

        if len(postData['last_name']) < 2:
            messages['name_errors'].append("Last name must be at least 2 characters!")
            failed_validation = True
        elif not NAME_REGEX.match(postData['last_name']):
            messages['name_errors'].append("Last name can only contain letters!")
            failed_validation = True

        try:
            found_user = User.objects.get(email=postData['email'])
        except:
            found_user = False

        if len(postData['email']) < 1:
            messages['email_errors'].append("Email is required!")
            failed_validation = True
        elif not EMAIL_REGEX.match(postData['email']):
            messages['email_errors'].append("Please enter a valid email!")
            failed_validation = True
        elif found_user:
            messages['email_errors'].append("This email is already registered!")
            failed_validation = True

        if failed_validation:
            return {'result':"failed_validation", 'messages':messages}

        if len(postData['password']) < 1:
            messages['password_errors'].append("Password is required!")
            failed_validation = True
        elif len(postData['password']) < 8:
            messages['password_errors'].append("Password must be at least 8 characters")
            failed_validation = True
        elif postData['confirm_password'] != postData['password']:
            messages['password_confirm_errors'].append("Password confirmation failed")
            failed_validation = True

        if failed_validation:
            return {'result':"failed_validation", 'messages':messages}

        return {'result':'success', 'messages':messages}




    def validate_identifier(self, identifier):

        print "*****************************************"
        print "Entered User.objects.validate_identifier"
        print "Recieved identifier ----->", identifier

        messages = []
        valid_email = False
        valid_phone = False

        if EMAIL_REGEX.match(identifier):
            valid_email = True
            print "Found valid email address"
        elif PHONE_REGEX.match(identifier):
            valid_phone = True
            print "Found valid phone number"
        else:
            messages.append("*Please enter a valid email or phone number!")
            print "ERROR: identifier didn't match EMAIL or PHONE regexes"
            return {'result':'failed_validation', 'messages':messages}

        if valid_email:
            try:
                print "Attempting to find user with entered email address..."
                user = User.objects.get(email=identifier)
                print "Found user ----->", user
                if user:
                    print "User exists, returning success result!"
                    messages.append("User exists for this email address")
                    return {'result':'success', 'messages':messages, 'identifier_type':'email', 'identifier':identifier}
            except:
                messages.append("*No user exists for this email address")
                return {'result':'failed_validation', 'messages':messages}
        elif valid_phone:
            try:
                print "Attempting to find user with entered phone number..."
                user = User.objects.get(phone_number=identifier)
                print "Found user ----->", user
                if user:
                    print "User exists, returning success result!"
                    messages.append("User exists for this phone number")
                    return {'result':'success', 'messages':messages, 'identifier_type':'phone', 'identifier':identifier}
            except:
                messages.append("*No user exists for this phone number")
                return {'result':'failed_validation', 'messages':messages}

        else:
            print "Phone number and email both invalid... this print statement should never appear"
            messages.append("ERROR: Failed validation")
            {'result':'failed_validation', 'messages':messages}


    def authenticate_login(self, postData):

        print "******************************"
        print "Entered User.objects.authenticate_login"
        print "PostData: ", postData
        print "identifier in postData:", postData['identifier']
        print "identifier_type in postData:", postData['identifier_type']
        print "password in postData:", postData['password']

        failed_authentication = False
        messages = []

        if len(postData['password']) < 8:
            # print "password is less than 8 characters"
            messages.append("Password must be at least 8 characters")
            return {'result':"failed_authentication", 'messages':messages}

        if postData['identifier_type'] == "email":
            user = User.objects.get(email=postData['identifier'])
        else:
            user = User.objects.get(phone_number=postData['identifier'])

        # hashed_password = bcrypt.hashpw(str(postData['password']), str(user.salt))

        # if user.password != hashed_password:
        if user.password != postData['password']:
            # print "found_user password doesn't match hashed password"
            messages.append("Incorrect password! Please try again")
            failed_authentication = True


        if failed_authentication:
            # print "authentication failed after password check"
            return {'result':"failed_authentication", 'messages':messages}
        else:
            # print "authentication succeeded, should be successfully logged in"
            messages.append('Successfully logged in!')
            return {'result':'success', 'messages':messages, 'user_id':user.id}






class User(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    RATHER_NOT_SAY = "R"
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (RATHER_NOT_SAY, 'Rather not say')
    )

    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100, default="$2b$12$jP5X3r5Ji0g8BtDRyfYee.")
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Please enter phone number in the format: +12223334444'
        )
    ])
    #master folder is assigned to user during registration and will always be their root folder from then on
    #master_folder = models.ForeignKey(Folder, related_name="master_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()






class Folder(models.Model):
    name = models.CharField(max_length=45)
    owner = models.ForeignKey(User, related_name="owned_folders")
    authorized_users = models.ManyToManyField(User, related_name="authorized_folders", blank=True, null=True)
    parent_folder = models.ForeignKey('self', related_name="child_folders", blank=True, null=True)
    is_in_trash = models.BooleanField(default=False)
    is_master_folder = models.BooleanField(default=False)
    stars = models.ManyToManyField(User, related_name="starred_folders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Root_Folder(models.Model):
    user = models.ForeignKey(User, related_name="master")
    folder = models.ForeignKey(Folder, related_name="master")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#
# class Nest_relation(models.Model):
#     parent_folder = models.ForeignKey(Folder, related_name="parent_folder_relationships")
#     child_folder = models.ForeignKey(Folder, related_name="child_folder_relationship")

def get_upload_file_name(instance, filename):
    return "%s" %(filename)



class File(models.Model):
    file_data = models.FileField(upload_to=get_upload_file_name)
    file_type = models.CharField(max_length=15)
    owner = models.ForeignKey(User, related_name="owned_files")
    authorized_users = models.ManyToManyField(User, related_name="authorized_files",blank=True, null=True)
    parent_folder = models.ForeignKey(Folder, related_name="child_files",blank=True, null=True)
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
