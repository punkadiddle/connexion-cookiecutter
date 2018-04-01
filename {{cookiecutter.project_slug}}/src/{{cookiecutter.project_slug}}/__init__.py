import connexion
import json
import pkg_resources
import yaml
import os
import sys
from cfenv import AppEnv
from flask import Config as FlaskConfig
from prance import ResolvingParser

import logging


try:
    # setuptools-scm generiert die Versionsnummer aus GIT-Metadaten
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    # package ist nicht installiert
    __version__ = '0.0.0'


class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level


def convertSettingValue(x):
    if x == 'true':
        return True
    elif x == 'false':
        return False
    else:
        return x


def cloudFoundryfyConfig(config: FlaskConfig):
    """ Optionale Anpassung der Flask-Konfiguration mit CF-Umgebung
    """
    cfenv = AppEnv()
    print(cfenv)


def main(global_config, **settings):
    """ WSGI-Server erzeugen und konfigurieren.
    """

    #engine = engine_from_config(settings, prefix='sqlalchemy.',
    #                            connect_args={'check_same_thread':False},
    #                            poolclass=StaticPool)
    #DBSession.configure(bind=engine)
    #Base.metadata.bind = engine

    # Ini-Konfiguration unterstüzt keine Filter, daher hier stderr-Ausgabe
    # auf Meldungen ab WARNING filtern.
    for handler in logging.getLogger().handlers:
        if handler.stream is sys.stderr:
            handler.addFilter(LevelFilter(logging.WARNING))
    
    appInfo = {
        'product_slug': __package__,
        'product_version': __version__,
    }

    # TODO: aus Beispielprojekt, obsolet?
    #apiFile = pkg_resources.resource_stream(__name__, 'schema/swagger.yml')
    #parsedDefinition = yaml.load(apiFile)
    #swaggerDefiniton = ResolvingParser(spec_string=json.dumps(parsedDefinition)).specification

    # extrat all flask.* configuration items
    flaskConfig = dict(map(lambda x: (x[0][6:], convertSettingValue(x[1])),
                        filter(lambda x: x[0].startswith('flask.'), settings.items())))
    DEBUG = flaskConfig.get('DEBUG', False)

    # create app instance
    connexionApp = connexion.App("{{cookiecutter.project_name}}", debug=DEBUG, swagger_ui=True)
    flaskApp = connexionApp.app

    # configure
    flaskApp.config.update(flaskConfig)
    cloudFoundryfyConfig(flaskApp.config)
    
    apiFile = pkg_resources.resource_filename(__name__, 'schema/actuator.yml')
    connexionApp.add_api(apiFile, strict_validation=False, validate_responses=True)
    apiFile = pkg_resources.resource_filename(__name__, 'schema/swagger.yml')
    connexionApp.add_api(apiFile, strict_validation=True, validate_responses=True)

    print(yaml.dump(flaskApp.config))

    if DEBUG:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension()
        toolbar.init_app(flaskApp)

    {% if cookiecutter.use_sql == 'yes' %}
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

    {% endif %}
    {% if cookiecutter.use_ui == 'yes' %}
    # simple web-ui page without swagger
    from .ui.hello import helloPage
    flaskApp.register_blueprint(helloPage)

    {% endif %}

    return flaskApp
