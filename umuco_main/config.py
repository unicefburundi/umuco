"""TwitterOAuth settings :
Create a new application at https://apps.twitter.com/app/new and make sure to use a callback url of http://127.0.0.1:8000/complete/twitter.

In the "django_social_project" directory, add a new file called config.py. Grab the Consumer Key (API Key) and the Consumer Secret (API Secret) from Twitter under the "Keys and Access Tokens" tab and add them to the config file like so:
"""

SOCIAL_AUTH_TWITTER_KEY = 'update me'
SOCIAL_AUTH_TWITTER_SECRET = 'update me'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'
SOCIAL_AUTH_LOGIN_URL = '/'

"""
Facebook uses OAuth2 for its auth process. Further documentation at Facebook development resources:

Register a new application at Facebook App Creation, don't use localhost as App Domains and Site URL since Facebook won't allow them. Use a placeholder like myapp.com and define that domain in your /etc/hosts or similar file.
"""

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'en_US'}

"""Recently Google launched OAuth2 support following the definition at OAuth2 draft. It works in a similar way to plain OAuth mechanism, but developers must register an application and apply for a set of keys. Check Google OAuth2 document for details.

When creating the application in the Google Console be sure to fill the PRODUCT NAME at API & auth -> Consent screen form.

"""
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_SCOPE = ['https://mail.google.com']
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS= {'access_type': 'offline'}

SOCIAL_AUTH_LOGIN_ERROR_URL = '/'