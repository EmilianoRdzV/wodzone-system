import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'unfold',                           # Must be before django.contrib.admin
    'unfold.contrib.filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core',
]

UNFOLD = {
    "STYLES": [
        lambda request: "/static/admin/wodzone-admin.css",
    ],
    "SITE_TITLE": "WodZone Admin",
    "SITE_HEADER": "WOD ZONE",
    "SITE_SUBHEADER": "Sistema de Gestión",
    "SITE_URL": "/",
    "SITE_ICON": None,
    "SITE_SYMBOL": "fitness_center",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "COLORS": {
        "font": {
            "subtle-light":  "107 114 128",
            "subtle-dark":   "156 163 175",
            "default-light": "17 24 39",
            "default-dark":  "243 244 246",
            "important-light":"11 17 33",
            "important-dark": "255 255 255",
        },
        "primary": {
            "50":  "255 240 240",
            "100": "255 220 220",
            "200": "255 180 180",
            "300": "255 130 130",
            "400": "255 80 80",
            "500": "204 0 0",
            "600": "180 0 0",
            "700": "150 0 0",
            "800": "110 0 0",
            "900": "80 0 0",
            "950": "50 0 0",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Gimnasio",
                "separator": True,
                "items": [
                    {
                        "title": "Miembros",
                        "icon": "person",
                        "link": "/admin/core/member/",
                    },
                    {
                        "title": "Rachas",
                        "icon": "local_fire_department",
                        "link": "/admin/core/streaks/",
                    },
                ],
            },
            {
                "title": "Sistema",
                "separator": True,
                "items": [
                    {
                        "title": "Usuarios Admin",
                        "icon": "manage_accounts",
                        "link": "/admin/auth/user/",
                    },
                ],
            },
        ],
    },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS — allow React dev server and same-origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_ALL_ORIGINS = DEBUG  # In dev, allow all

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Primary DB: SQLite (local)
DB_LOCATION = os.getenv('DB_PATH', str(BASE_DIR / 'db.sqlite3'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_LOCATION,
    }
}


AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}
