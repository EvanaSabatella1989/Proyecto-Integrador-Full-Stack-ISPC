import os
from pathlib import Path
from datetime import timedelta




# configuracion para el envio de correos a  Mailtrap y hacer las pruebas
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'  # Servidor SMTP de Mailtrap
EMAIL_PORT = 2525  # Puerto de Mailtrap (Usa 587 si necesitas TLS)
EMAIL_HOST_USER = 'c1e209a5685478'  # Copia el usuario desde Mailtrap
EMAIL_HOST_PASSWORD = '458a83918d03ff'  # Copia la contraseña desde Mailtrap
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # No usar SSL  



# evitar que se cierre sesion 
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  
    'ROTATE_REFRESH_TOKENS': True,               
    'BLACKLIST_AFTER_ROTATION': True,            
    'UPDATE_LAST_LOGIN': True,                   
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ue_9_cd$j!ezi1(i07f)u_6qr*c_2#p(ef7n%&5f!(b_-mh5d$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'rest_framework_simplejwt',
    'producto',
    'categoria',
    'venta',
    'venta_detalle',
    'sucursal',
    'turno',
    'reserva',
    'servicio',
    'vehiculo',
    'rest_framework',
    "corsheaders",
    'carrito',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_autoservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'api_autoservice.wsgi.application'

# CORDS
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
]
CORS_ALLOW_ALL_ORIGINS = True  # Habilita CORS para todas las solicitudes
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
]

# Database

DATABASES = {
   
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'autoservice',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# para que la imagen cargue
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'static', 'static-only')

STATICFILES_DIRS = [
    # BASE_DIR / 'photos',
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
]

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)),
                 'static', 'templates'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "user.UserAccount"


# REST_FRAMEWORK = {
#   'DEFAULT_AUTHENTICATION_CLASSES': (
#      'rest_framework_simplejwt.authentication.JWTAuthentication',
# )
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
}

APPEND_SLASH = False
