#@PydevCodeAnalysisIgnore

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
        }
}

INSTALLED_APPS = ['flows', 'flows.statestore.tests']

SECRET_KEY = 'flow_tests'


try:
    import django_jenkins
    INSTALLED_APPS += ('django_jenkins',)
    # django_jenkins will test and run reports for PROJECT_APPS only
    PROJECT_APPS = ('flows',)
except ImportError:
    pass
