import logging
from flask import request, current_app, url_for


logger = logging.getLogger(__package__)


def get():
    prefix = request.blueprint

    result = {}
    rules = current_app.url_map.iter_rules()
    for rule in rules:
        try:
            if rule.rule.startswith(prefix):
                name = rule.rule[len(prefix):].strip('/')
                if not name:
                    name = 'self'
                result[name] = { 'href': url_for(rule.endpoint, _external=True) }
                
        except:
            logger.exception("problem scanning rules")
        
    return {'_links': result}
