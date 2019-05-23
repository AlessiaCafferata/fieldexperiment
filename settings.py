from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
       'name': 'fondo_pensioni',
       'display_name': "Fondo pensioni",
       'num_demo_participants': 6,
       # 'num_demo_participants': 2,
       'app_sequence': ['fondo_pensioni', ],
       'use_browser_bots': False,  # XXX settare a False!
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2

USE_POINTS = True
POINTS_DECIMAL_PLACES = 2
POINTS_CUSTOM_NAME = ""

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'o1)t8w&37h*3l7tc!li2xff05kt5l)lwzpvju-y*gx9ic5rq9*'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'fondo_pensioni']

# Required for DEBUG = False
ALLOWED_HOSTS = ['*']

DEBUG = False
