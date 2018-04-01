.PHONY: clean test start_dev

all: test

Pipfile:
	# Cloud Foundry Python Buildpack verwendet pipenv.
	# Pipfile soll requirements.txt ablösen, ist aber noch instabil. Aktuell ist setup.cfg
	# führend (https://github.com/pypa/pipfile).
	pipenv --three install -e "${PWD}"
	#python3 -m virtualenv --clear venv
	#venv/bin/pip install -e .

venv: Pipfile

clean:
	pipenv clean
	rm -rfv bin develop-eggs dist downloads .eggs venv parts vendor
	rm -fv Pipfile Pipfile.lock
	rm -fv .coverage .installed.cfg bootstrap.py requirements.txt 
	rm -fv logs/*.txt
	find . -name '*.pyc' -or -name '*.pyo' -exec rm -fv {} \;
	find . -type d -depth -name '*.egg-info' -or -name '__pycache__' -exec rm -rfv {} \;

start: Pipfile
	pipenv run gunicorn --paste production.ini

start_dev: Pipfile
	pipenv run gunicorn --paste development.ini

vendor:
	# Speichert die aktuelle Konfiguration an Abhängigkeiten als requirements.txt
	# und speichert alle Abhängigkeiten im Ordner vendor.
	# -> Cloud Foundry Offline Deployment
	pipenv run pip freeze --local
	pipenv run pip download --dest vendor --no-binary :all: .



{% if cookiecutter.use_docker.startswith('y') -%}
build-docker:
	docker build -t {{cookiecutter.docker_repository}}{{'/' if cookiecutter.docker_repository else ''}}{{cookiecutter.docker_project_name}}:{{cookiecutter.docker_default_tag}} .

build-and-push: build-docker
	docker push {{cookiecutter.docker_repository}}{{'/' if cookiecutter.docker_repository else ''}}{{cookiecutter.docker_project_name}}:{{cookiecutter.docker_default_tag}}

start-docker:
	docker rm {{cookiecutter.project_slug}} || true
	docker run --name "{{cookiecutter.project_slug}}" -p "127.0.0.1:{{cookiecutter.api_port}}:{{cookiecutter.api_port}}" {{cookiecutter.docker_repository}}{{'/' if cookiecutter.docker_repository else ''}}{{cookiecutter.docker_project_name}}:{{cookiecutter.docker_default_tag}}

attach-to-docker:
	 docker exec -i -t {{cookiecutter.project_slug}} /bin/bash 
{%- endif %}
	
update: Pipfile
	pipenv update

test: Pipfile
	pipenv run python setup.py pytest --addopts --cov={{cookiecutter.project_slug}}
