"""
Django settings for SMonitor project.
Settings for developement environment

"""

from Config.settings.production import * 


APPEND_SLASH = True
INSTALLED_APPS += [
    # Third party
    'rest_framework_swagger',
]

#SWAGGER_SETTINGS = {
#    }
#LOGIN_URL = 'accounts:login',
#LOGOUT_URL = 'accounts:logout',
