=================
Django Inteliger
=================

Django Inteliger e um pacote da www.inteliger.com.br para todo mundo
aprender como fazer uma boa estruturacao de codigo.


Como usar
-----------

1. Adicione os aplicativos do pacote no seu INSTALED_APPS.

    INSTALLED_APPS = [
        ...
        'core',
        'log',
        'usr',
        'filial'

    ]

2. Adicione o middleware de log no MIDDLEWARE.

    MIDDLEWARE = [
        ...
        'log.middleware.LogMiddleWare'

    ]

3. Rode ``python manage.py migrations`` para criar as migracoes

4. Rode ``python manage.py migrate`` para criar as tabelas

5. Aproveite