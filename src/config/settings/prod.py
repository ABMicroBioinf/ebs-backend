""" DEBUG = False
ALLOWED_HOSTS = ['******']
# Database connection to Azure URL
DATABASES = settings.DATABASES
DATABASES['default'] = dj_database_url.parse('******', conn_max_age=500,
                                             ssl_require=True)
# For django storages
AZURE_ACCOUNT_NAME = ******
AZURE_ACCOUNT_KEY = ******
AZURE_CONTAINER = ******
SHARE_URL = "******"
AZURE_BLOB_CUSTOM_DOMAIN = '******'
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = '******'
STATIC_URL = "https://%s/%s/" % (AZURE_BLOB_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = '******'
MEDIA_URL = "https://%s/%s/" % (AZURE_BLOB_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
 """


from tutorial.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ebsdb',
        'ENFORCE_SCHEMA': False,
    }
}

# CORS
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:3000'
]
CORS_ALLOW_CREDENTIALS = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': JWT_SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 'USER_ID_FIELD': 'email',
    # 'USER_ID_CLAIM': 'email',
    'USER_ID_FIELD': '_id',
    'USER_ID_CLAIM': '_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    'AUTH_COOKIE_HTTP_ONLY' : True,
    'AUTH_COOKIE_SAMESITE': 'Strict',
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SECURE': not DEBUG,
    'AUTH_COOKIE_DOMAIN': None,
    #'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE': 'auth_token',
}












# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Edmonton'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static_cdn')
MEDIA_ROOT = os.path.join(BASE_DIR, '../media_cdn')

try:
    from tutorial.settings.local import *
except:
    pass
