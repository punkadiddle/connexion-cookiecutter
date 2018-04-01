# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

The API is running at ```http://localhost:{{cookiecutter.api_port}}/api/v1```.

Go to [here](http://localhost:8080/api/v1/ui) to view the brilliant SwaggerUI documentation of your API.

A simple non-api Web-Page is running at ```http://localhost:{{cookiecutter.api_port}}/hello```.

## Verwendung

### Installation

Run ```make``` for a local setup and then ```make start_dev``` to start the API in debug mode.

To start the uWSGI, run ```make start```


### Procedure

First, define your REST API in the configuration under ```/config/api.yml```, 
then add the Python logic for the *operationId* under /{{cookiecutter.project_slug}}/api

### Healthcheck

Configure a health check under /api/v1/health (GET).

The check should return 200 if everything is fine, 424 if a depending service is not working or 503 if the API does not work correctly.
Additionally, a JSON is returned containing the fields 'health', 'dependencies' and 'message'. The first one defines the color ('green', 'yellow', 'red') that
correspond to the status codes. The second one is the name of the depending services that cannot be reached and 'message'
can hold a string defining the cause of a problem.

### Scripts
`make` Build project

`make clean` Clean folder

`make test` Run tests

`make start` / `make start_dev` mit Produktions- oder Entwicklungskonfiguration starten

`make build-and-push` Build Docker image and push to repository

## Deployment

## Cloud Foundry

Der Service ist zum Deployment auf Cloud Foundry vorkonfiguriert. Deploymentprozedur:

 1. Download der Abhängigkeiten: ``make vendor test``
 2. Push ``cf push``


Folgende Dateien konfigurieren das Buildpack:

 * `manifest.yml`
 * `Procfile`
 * `runtime.txt`

{%- if cookiecutter.use_docker.startswith('y') -%}
## Docker

If configured, a Dockerfile ist autmatically generated at the project root. Call ``make build-docker`` to build a new image or 
``make build-and-push`` to upload the image to the registry afterwards. 

In case you want to run a container locally, run ``make start-docker``. With ``make attach-to-docker`` you can easily open a bash
on the running container.
{%- endif %}


## Testing

### Benchmarks

```sh
wrk -d5s -t10 -c200 http://localhost:8080/api/v1/health
```

## Weiterführende Informationen

### API Design
[Google Cloud API Designanleitung](https://cloud.google.com/apis/design/)
[Zalando API Guidelines](https://zalando.github.io/restful-api-guidelines/)
[API.yml Editor](http://editor.swagger.io/#/)

### gUnicorn
[Tutorial: gUnicorn behind Nginx](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx)

### Connexion
[Documentation](https://connexion.readthedocs.io/en/latest/)
[Repository](https://github.com/zalando/connexion)
