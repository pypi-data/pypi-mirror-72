=================
Django Inteliger
=================

Django Inteliger e um pacote da Inteliger para todo mundo
aprender como fazer uma boa estruturacao de codigo.


Como usar
-----------

1. Adicione os aplicativos do pacote no seu INSTALED_APPS.

    INSTALLED_APPS = [
        ...
        'core',
        'log',
        'usr'

    ]

2. Adicione o middleware de log no MIDDLEWARE, antes de todos os outros.

    MIDDLEWARE = [
        'log.middleware.LogMiddleware',
        ...

    ]

3. Adicione as urls no urlpatterns.

    urlpatterns = [
        ...
        re_path(r'^usr/', include('usr.urls')),
        re_path(r'^core/', include('core.urls')),
        re_path(r'^log/', include('log.urls'))

    ]


4. Rode ``python manage.py migrate`` para criar as tabelas

5. Aproveite