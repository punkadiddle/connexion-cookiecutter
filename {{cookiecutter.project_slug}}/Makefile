.PHONY: clean update test run rundev vendor ssh push {% if cookiecutter.use_docker.startswith('y') %}build-docker start-docker attach-to-docker{% endif %}

all: test startdev

clean:
	pipenv clean
	rm -rfv develop-eggs dist downloads .eggs venv parts vendor
	rm -fv .coverage .installed.cfg bootstrap.py requirements.txt 
	find . -name '*.pyc' -or -name '*.pyo' -exec rm -fv {} \;
	find . -type d -depth -name '*.egg-info' -or -name '__pycache__' -exec rm -rfv {} \;

Pipfile.lock:
	PIPENV_VENV_IN_PROJECT=1 pipenv --three install --dev
	pipenv install -e .

venv: clean Pipfile.lock

update: Pipfile
	pipenv update

test: Pipfile
	pipenv run python setup.py pytest --addopts --cov={{cookiecutter.project_slug}}

run: Pipfile
	pipenv run gunicorn --paste production.ini

rundev: Pipfile
	pipenv run gunicorn --paste development.ini

vendor:
	# Speichert die aktuelle Konfiguration an Abhängigkeiten als requirements.txt
	# und speichert alle Abhängigkeiten im Ordner vendor.
	# -> Cloud Foundry Offline Deployment
	pipenv lock -r > requirements.txt
	pipenv run pip download --dest vendor -r requirements.txt --no-binary :all: 

push: vendor
	cf push

ssh:
	echo "SSH funktioniert nur, während der Container läuft."
	echo "Die Python-Umgebung an einem laufenden Prozess auslesen:"
	echo "cat /proc/\\$(ps aux | grep gunicorn | grep -v grep | head -n1 | awk '{ print \\$2 }')/environ | tr \\\\0 \\\\n"
	echo ""
	cf ssh {{cookiecutter.project_slug}}

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
	
