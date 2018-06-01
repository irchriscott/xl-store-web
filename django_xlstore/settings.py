import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '74o-2+lzxsi0&luu8^w5!@m%0av5g73fsy41^l(&!diq!#a6pz'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ["*"]

#EMAIL SET UP TOOLS

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'ms.xlstore@gmail.com'

EMAIL_HOST_PASSWORD = '323639371998'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
    'django.contrib.humanize',
    'xlstore',
    #'xlstoreapi',
    'xlstore_managment',
    'xlstore_ecommerce',
]

DELETE_MESSAGE = 50

MESSAGE_TAGS = {
    DELETE_MESSAGE : 'Deleted'
}

AUTH_USER_MODAL = 'xlstore.Company'

AUTHENTIFICATION_BACKENDS = ('xlstore.backends.CompanyAuth',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_xlstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_xlstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xlstoredb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST':'localhost',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_files')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'assets'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PAGINATOR_ITEMS = 4

TRADE_STATUSES = [
                    (1,"started"),
                    (2,"stopped"),
                    (3,"aborted"),
                    (4,"failed"),
                    (5,"succeeded")
                 ]

MARKET_ACCESS_STATUSES = [
                            (1, "allowed"),
                            (2, "disallowed"),
                            (3, "blocked"),
                            (4, "vip")
                        ]

CART_STATUSES = [
                    (1, "created"),
                    (2, "finished"),
                    (3, "suspended"),
                    (4, "accepted"),
                    (5, "paid"),
                    (6, "delivered")
                ]


MOBILE_MONEY_AIRLINES = [
                            {
                                "country": "CD",
                                "code": "+243",
                                "airlines": [
                                    {
                                        "name": "Airtel",
                                        "code": ["99", "97"]
                                    },
                                    {
                                        "name": "Orange",
                                        "code": ["85", "84"]
                                    },
                                    {
                                        "name": "Vodacom",
                                        "code": ["81", "80"]
                                    }
                                ]
                            },
                            {
                                "country": "UG",
                                "code": "+256",
                                "airlines": [
                                    {
                                        "name": "Airtel",
                                        "code": ["75", "70"]
                                    },
                                    {
                                        "name": "MTN",
                                        "code": ["87", "34"]
                                    },
                                    {
                                        "name": "Africell",
                                        "code": ["40", "41"]
                                    }
                                ]
                            }
                        ]

