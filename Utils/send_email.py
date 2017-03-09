from django.core.mail import send_mail
from django.conf import settings

# Python Related Library
import os
import binascii

def send_email_with_token(base_url, title, content, email):
    # Construct a url with a random generate token, then send it to the user's email
    token = binascii.b2a_hex(os.urandom(15)).decode('utf-8')
    if settings.HOST:
        url = HOST + base_url + '?code=' + token
    else:
        url = '127.0.0.1:8000' + base_url + '?code=' + token
    # Send the request user an email, and set the token 
    result = send_mail(title, content +  url, 'emailsniff@163.com', [email,], fail_silently=True)
    return token, result
