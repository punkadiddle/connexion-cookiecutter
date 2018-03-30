.PHONY: clean start {% if cookiecutter.use_docker.startswith('y') %}build-docker build-and-push start-docker attach-to-docker{% endif %}

all: venv/bin/python

venv/bin/python:
	python3 -m virtualenv venv
	venv/bin/pip -e .

clean:
	rm -rfv bin develop-eggs dist downloads .eggs venv parts
	rm -fv .coverage .installed.cfg bootstrap.py
	rm -fv logs/*.txt
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;

start: venv/bin/python
	venv/bin/gunicorn --paste development.ini

vendor:
	venv/bin/pip install --download vendor --no-binary :all:

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
{%- endif -%}

update-all-packages: venv/bin/python
	 env/bin/pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 env/bin/pip install -U

test: venv/bin/python
	venv/bin/python setup.py pytest --addopts --cov={{cookiecutter.project_slug}}
	
