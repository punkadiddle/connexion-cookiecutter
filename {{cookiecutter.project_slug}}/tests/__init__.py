from {{cookiecutter.project_slug}} import main


# Get Flask app
flaskApp = main({})
flaskApp.testing = True
client = flaskApp.test_client()
