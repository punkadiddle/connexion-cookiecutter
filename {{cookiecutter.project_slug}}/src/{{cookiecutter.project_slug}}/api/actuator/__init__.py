import logging
from .. import getBlueprintIndex


logger = logging.getLogger(__package__)


def get():
    """ Index der nachgelagerten Einträg erstellen. """

    result = getBlueprintIndex()
    return {'_links': result}, 200
