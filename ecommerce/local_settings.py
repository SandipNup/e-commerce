DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'e_com',

          'USER': 'amnil1',

          'PASSWORD': 'amnil123',

          'HOST': 'localhost',

          'PORT': '5432',
    }
}

AUTH_USER_MODEL = 'shop.User'