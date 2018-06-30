from flask import Blueprint
from .. import appInfo


helloPage = Blueprint('hello', __name__, template_folder='')


@helloPage.route("/<page>")
def hello(page):

    return """
    <html><body>
    <h1>Hello World</h1>
    <p>This is an annoying page that shows up everywhere else and also at '%s'!</p>
    <code>%s</code>
    </body></html>
    """ % (page, appInfo)
