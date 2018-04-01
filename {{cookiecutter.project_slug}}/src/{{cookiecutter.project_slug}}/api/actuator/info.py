from {{cookiecutter.project_slug}} import __version__ as appVersion


def get():
    return {
        "build": {
            "artifact": "",
            "group": "",
            "name": "{{cookiecutter.project_slug}}",
            "version": appVersion,
            "time": 42,
        }
    }, 200
