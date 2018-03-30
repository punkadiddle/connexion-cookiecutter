from flask import Blueprint


helloPage = Blueprint('hello', __name__, template_folder='')


@helloPage.route("/<page>")
def hello(page):
    return "<html><body>Hello World!</body></html>"
