#! /usr/bin/python3
# -*- coding: utf-8 -*-
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from .models import User

class EmailOrUsernameModelBackend(object):
    """
    Authentication with either a username or an email address, key as username

    """
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
