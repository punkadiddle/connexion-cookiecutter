import connexion
import pkg_resources
import logging
import yaml
import os
import sys
from cfenv import AppEnv
from flask import Config as FlaskConfig


logger = logging.getLogger(__package__)

try:
    # setuptools-scm generiert die Versionsnummer aus GIT-Metadaten
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    # package ist nicht installiert
    __version__ = '0.0.0'


def pasteToFlaskConfig(global_config, settings):
    def __convVal(x):
        if x == 'true':
            return True
        elif x == 'false':
            return False
        else:
            return x

    incfg = global_config.copy()
    incfg.update(settings)

    outcfg = dict(map(lambda x: (x[0][6:], __convVal(x[1])),
                  filter(lambda x: x[0].startswith('flask.'), incfg.items())))
    
    return outcfg


def cloudFoundryfyConfig(config: FlaskConfig):
    """ Optionale Anpassung der Flask-Konfiguration mit CF-Umgebung
    """
    cfenv = AppEnv()
    if len(cfenv.app) > 0:
        logger.info("app %s %d services: %s", cfenv.name, len(cfenv.services), cfenv.app)
        for service in cfenv.services:
            logger.info("bound service '%s': %s", service.name, service.env)

        {% if cookiecutter.use_reldb.startswith('y') -%}
        vcapdb = cfenv.get_service(label='p-mysql')
        if vcapdb:
            logger.info("%s", vcapdb)
            config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{hostname}:{port}/{name}'.format(
                **vcapdb.credentials)
            logger.info("MySQL Service %s konfiguriert", vcapdb.credentials['hostname'])

        elif 'SQLALCHEMY_DATABASE_URI' not in config:
            logger.critical("Kein Datenbank-Service gebunden!")
        {%- endif %}

    else:
        cfenv = None

    return cfenv


def main(global_config, **settings):
    """ WSGI-Server erzeugen und konfigurieren.
    """
    appInfo = {
        'product_slug': __package__,
        'product_version': __version__,
    }

    # extrat all flask.* configuration items
    flaskConfig = pasteToFlaskConfig(global_config, settings)
    DEBUG = flaskConfig.get('DEBUG', '0') in ['1', 'on', 'true']
    VERBOSE = int(global_config.get('STARTUP_VERBOSE', 0))

    # create app instance
    connexionApp = connexion.App("{{cookiecutter.project_name}}", debug=DEBUG, swagger_ui=True)
    flaskApp = connexionApp.app

    # configure
    flaskApp.config.update(flaskConfig)
    cloudFoundryfyConfig(flaskApp.config)
    
    # Rest-Endpoint CF Spring Actuator like Metadaten (Definition im sub-package api.actuator)
    apiFile = pkg_resources.resource_filename(__name__, 'schema/actuator.yml')
    connexionApp.add_api(apiFile, strict_validation=False, validate_responses=True,
                         resolver=connexion.RestyResolver('%s.api.actuator' % (__package__)),
                         base_path='/cloudfoundryapplication')

    # Restendpoint App Version 1 (Definition im sub-package api)
    apiFile = pkg_resources.resource_filename(__name__, 'schema/app_v1.yml')
    connexionApp.add_api(apiFile, strict_validation=True, validate_responses=True,
                         resolver=connexion.RestyResolver('%s.api' % (__package__)))

    if VERBOSE > 0:
        print(yaml.dump(flaskApp.config))

    if DEBUG:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension()
        toolbar.init_app(flaskApp)

    {% if cookiecutter.use_reldb.startswith('y') %}
    # proaktive Initialisierung der Datenbank (entfernen -> lazy)
    from .model import getDb
    with flaskApp.app_context():
        db = getDb()
    {% endif -%}

    {% if cookiecutter.use_ui.startswith('y') %}
    # simple web-ui page without swagger
    from .ui.hello import helloPage
    flaskApp.register_blueprint(helloPage)
    {% endif -%}

    return flaskApp
