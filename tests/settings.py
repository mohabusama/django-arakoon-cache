
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'tests.cache_app'
)

CACHES = {
    'default': {
        'BACKEND': 'django_arakoon_cache.cache.ArakoonCache',
        'LOCATION': {
            'arakoon_0': ('127.0.0.1', 4000),
            'arakoon_1': ('127.0.0.1', 4001),
            'arakoon_2': ('127.0.0.1', 4002)
        },
        'OPTIONS': {
            'cluster': 'django'
        }
    }
}
