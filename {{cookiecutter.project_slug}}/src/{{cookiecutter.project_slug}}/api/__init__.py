import logging
from flask import request, current_app, url_for
from werkzeug.routing import BuildError
from typing import Dict


logger = logging.getLogger(__package__)


def getBlueprintIndex(prefix: str=None) -> Dict[str, str]:
    """ Erzeugt ein Dictionary der Seiten unterhalb von <prefix>. """

    if prefix is None:
        prefix = request.blueprint

    result = {}
    rules = current_app.url_map.iter_rules()
    for rule in rules:
        try:
            if rule.rule.startswith(prefix):
                name = rule.rule[len(prefix):].strip('/')
                if not name:
                    name = 'self'
                elif '/' in name:
                    continue
                result[name] = {'href': url_for(rule.endpoint, _external=True)}
                
        except BuildError as ex:
            # Die internen swagger_ui seiten werfen Fehler, die aber nicht relevant sind.
            logger.debug("problem scanning rules", exc_info=ex)

    return result
