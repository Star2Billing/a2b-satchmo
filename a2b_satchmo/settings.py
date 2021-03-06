# Django settings for mysite project.
import os

#DIRNAME = os.path.dirname(__file__)
DIRNAME = os.path.abspath(os.path.dirname(__file__))

DJANGO_PROJECT = 'a2b_satchmo'
DJANGO_SETTINGS_MODULE = 'a2b_satchmo.settings'

APPLICATION_DIR = os.path.dirname( globals()[ '__file__' ] )
GRAPPELLI_ADMIN_TITLE = 'A2Billing Administration'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql', # django.db.backends Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'customer_a2b', # django_test Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'shrenik',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    #'test1': {
    #    'ENGINE': 'mysql', # django.db.backends Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    #    'NAME': 'django-a2b', # django_test Or path to database file if using sqlite3.
    #    'USER': 'root',                      # Not used with sqlite3.
    #    'PASSWORD': 'password',                  # Not used with sqlite3.
    #    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    #    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    #},
}
																																																																																																																																	

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# MEDIA_ROOT = ''
MEDIA_ROOT = os.path.join( APPLICATION_DIR, 'resources' )
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = ''
MEDIA_URL = '/resources/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rc^gmr7x^p_=!@8pg5@9$2^%@-xetrni$v@nn^pcd!7+!#b-0)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    "django.middleware.doc.XViewMiddleware",
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #"threaded_multihost.middleware.ThreadLocalMiddleware",
    "satchmo_store.shop.SSLMiddleware.SSLRedirect",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    'satchmo_store.shop.context_processors.settings',
)

ROOT_URLCONF = 'a2b_satchmo.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join( APPLICATION_DIR, 'templates' ), 
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False,
}

INSTALLED_APPS = (
    #'admin_tools',
    #'admin_tools.theming',
    #'admin_tools.menu',
    #'admin_tools.dashboard',

    #'grappelli',
    
    'satchmo_store.shop',
    
    'django.contrib.auth',    
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.flatpages',    
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    #'django.contrib.databrowse',
    
    'registration',
    'sorl.thumbnail',
    'keyedcache',
    'livesettings',
    'l10n',    
    #'satchmo_utils.thumbnail',
    'satchmo_store.contact',

    'tax',
    #'tax.modules.no',
    #'tax.modules.area',
    'tax.modules.percent',
    'tax.modules.us_sst',
    
    'shipping',
    'shipping.modules.no',

    'product',
    'product.modules.configurable',
    'product.modules.custom',
    'product.modules.subscription',

    'payment',
    'payment.modules.dummy',
    'payment.modules.autosuccess',
    'payment.modules.cod',
    'payment.modules.purchaseorder',
    'payment.modules.paypal',
    #'payment.modules.authorizenet',
    'payment.modules.google',
    'satchmo_ext',
    'satchmo_ext.recentlist',
    #'satchmo_ext.satchmo_toolbar',
    'satchmo_ext.newsletter',
    #'satchmo_ext.newsletter.simple',
    #'satchmo_ext.newsletter.mailman',
    'satchmo_utils',
    'app_plugins',
    'a2b_satchmo.localsite',
   
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'dilla',
    #'debug_toolbar',
    #'django_extensions',
    'pagination',
    'dateutil',
    'uni_form',
    'a2b_satchmo.customer',
    #'paypal.standard.ipn', 
    'a2b_satchmo.api',
    'django_extensions',
    #'django_cron',
    #'staticfiles',
)


#ADMIN_TOOLS_MENU = 'a2b_satchmo.menu.CustomMenu'
#ADMIN_TOOLS_INDEX_DASHBOARD = 'a2b_satchmo.dashboard.CustomIndexDashboard'
#ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'a2b_satchmo.dashboard.CustomAppIndexDashboard'
#ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'

PAYPAL_RECEIVER_EMAIL = "yourpaypalemail@example.com"


LANGUAGES = (
    ('en', 'English'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('br', 'Brazilian'),
)

L10N_SETTINGS = {

}

ADMIN_REORDER = (
    ("customer", ("Card","SipBuddies" ,"IaxBuddies","Callerid","Cardgroup","Speeddial")),
    ("call_report", ("Call",)),
    ("system_settings", ("Config", "ConfigGroup")),
)

#### Satchmo unique variables ####
from django.conf.urls.defaults import patterns, include
SATCHMO_SETTINGS = {
    'SHOP_BASE' : '',
    'MULTISHOP' : False,
    #'SHOP_URLS' : patterns('satchmo_store.shop.views',)
    'SHOP_URLS' : patterns('', (r'^i18n/', include('l10n.urls')),)

}

AUTHENTICATION_BACKENDS = (
    'satchmo_store.accounts.email-auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend'
    )


gettext = lambda s: s


try :
    #from settings_local import *
    from local_settings import *
except :
    pass


try :
    from settings_local import *
except :
    pass



