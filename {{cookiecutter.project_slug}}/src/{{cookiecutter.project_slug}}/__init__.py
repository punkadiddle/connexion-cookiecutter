import connexion
import json
import pkg_resources
import yaml
import os
from flask import Config as FlaskConfig
from prance import ResolvingParser

from .notapi.hello import helloPage


def convertSettingValue(x):
    if x == 'true':
        return True
    elif x == 'false':
        return False
    else:
        return x


def cloudFoundryfyConfig(config: FlaskConfig):
    print(os.getenv('VCAP_SERVICES', ''))


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    #engine = engine_from_config(settings, prefix='sqlalchemy.',
    #                            connect_args={'check_same_thread':False},
    #                            poolclass=StaticPool)
    #DBSession.configure(bind=engine)
    #Base.metadata.bind = engine

    apiFile = pkg_resources.resource_stream(__name__, 'schema/swagger.yml')
    parsedDefinition = yaml.load(apiFile)
    swaggerDefiniton = ResolvingParser(spec_string=json.dumps(parsedDefinition)).specification

    # extrat all flask.* configuration items
    flaskConfig = dict(map(lambda x: (x[0][6:], convertSettingValue(x[1])),
                        filter(lambda x: x[0].startswith('flask.'), settings.items())))
    DEBUG = flaskConfig.get('DEBUG', False)

    # create app instance
    app = connexion.App("{{cookiecutter.project_name}}", debug=DEBUG, swagger_ui=True)
    flaskApp = app.app

    # configure
    flaskApp.config.update(flaskConfig)
    cloudFoundryfyConfig(flaskApp.config)
    app.add_api(swaggerDefiniton, strict_validation=False, validate_responses=False)
    print(yaml.dump(flaskApp.config))

    if DEBUG:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension()
        toolbar.init_app(flaskApp)

    {%- if cookiecutter.use_sql == 'yes' %}
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

    {% endif %}
    # simple web-ui page without swagger
    flaskApp.register_blueprint(helloPage)

    return flaskApp
