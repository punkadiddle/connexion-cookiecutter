# API-First Python Webservice Cookiecutter-Template

This Cookiecutter template helps you setting up a RESTful API in minutes. Just answer some questions about you and your projects and a ready-to-go python project will be created.

## Voraussetzungen

- Python 3 mit pip
- Cookiecutter

## Verwendung

```bash
# Voraussetzungen installieren
sudo apt install python3-pip
pip3 install --user cookiecutter pipenv

# Projekt anlegen
cookiecutter https://github.com/jgontrum/connexion-cookiecutter.git

# Starten
cd <PROJECTNAME>/
make start_dev
```

## Features

- Ready-to-go **Python 3.6** project
  - Flask Restful API Bepisiel
  - Pastedeploy Konfiguration
  - Makefile mit den wichtigesten Build- und Deploymentfunktionen
  - _optional_: Flask Web-UI Beispiel
  - _optional_: SQLAlchemy DB Abstraktionslayer
- Integration mit **Swagger 2.0** [API-First Ansatz](https://zalando.github.io/restful-api-guidelines/) ([Connexion](https://github.com/zalando/connexion))
  - Strict **model validation** by default
  - Swagger API UI-Konsole
- Testumgebung
  - Examples for **unit and integration tests**
  - **Coverage reports** for tests
  - Konfiguration für **SonarQube**
- Editorunterstützung
  - Konfiguration für **Eclipse PyDev** (unterstüzt Debugging)
  - Konfiguration für **Visual Studio Code** (Debugging instabil v1.21.1)
- Deploymentkonfigurationen
  - Setuptools/Egg Paketierung
  - Konfiguration für **Cloud Foundry** Deployment
  - _optional_: **Dockerfile** / Docker Build
    - gunicorn wsgi app behind nginx
    - direct support for static files (-> nginx)


### Todos
- SQLAlchemy
- Cloud Foundry 2.0 testen (aktuell: PCF Dev 1.11)
- Cloud Foundry 2.0 [multi-buildpack Support](https://docs.cloudfoundry.org/buildpacks/use-multiple-buildpacks.html) für statische Dateien analog Docker konfigurieren
- Eureka Service Client
