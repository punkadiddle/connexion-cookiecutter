from {{cookiecutter.project_slug}}.app import app


# Get Flask app
flaskApp = main({})
flaskApp.testing = True
client = flaskApp.test_client(
