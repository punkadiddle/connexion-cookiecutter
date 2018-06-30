PROJECT_SLUG={{cookiecutter.project_slug}}

.PHONY: clean delete pipeline push run rundev ssh sonarqube test update

# install pipenv to create .venv directory
.venv: Pipfile
	PIPENV_VENV_IN_PROJECT=1 pipenv --three install --dev

# change in Pipfile requires to rebuild Pipfile.lock
Pipfile.lock: .venv Pipfile
	pipenv update

requirements.txt: Pipfile.lock
	# Speichert die aktuelle Konfiguration an Abhängigkeiten als requirements.txt
	# und speichert alle Abhängigkeiten im Ordner vendor.
	# -> Cloud Foundry Offline Deployment
	pipenv lock -r > requirements.txt
	# lokales Paket nicht nochmal packen...
	grep -v '^-e' requirements.txt > requirements-vendor.txt
	pipenv run pip download --dest vendor -r requirements-vendor.txt --no-binary :all: 
	rm requirements-vendor.txt

all: Pipfile.lock

clean:
	rm -rfv develop-eggs dist downloads .eggs .venv parts vendor
	rm -fv .coverage .installed.cfg bootstrap.py requirements.txt test-coverage.xml test-report.xml pylint-report.txt
	find . -name '*.pyc' -or -name '*.pyo' -exec rm -fv {} \;
	find . -type d -depth -name '*.egg-info' -or -name '__pycache__' -exec rm -rfv {} \;

install: .venv

update: Pipfile.lock

test: Pipfile.lock
	pipenv run python setup.py pytest --addopts --cov=$(PROJECT_SLUG)

run: Pipfile.lock
	pipenv run gunicorn --paste production.ini

rundev: Pipfile.lock
	pipenv run gunicorn --paste development.ini

push: requirements.txt
	cf push

restage: requirements.txt
	cf restage $(PROJECT_SLUG)

delete:
	cf delete $(PROJECT_SLUG) -f

pipeline:
	fly -t local set-pipeline --non-interactive --pipeline "$(PROJECT_SLUG)" \
		--config=ci/pipeline.yml \
		--load-vars-from=ci/common/params.yml \
		--load-vars-from=ci/project-params.yml

sonarqube: test
	pipenv run pylint --output-format text --msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' src | tee pylint-report.txt
	sonar-scanner

ssh:
	echo "SSH funktioniert nur, während der Container läuft."
	echo "Die Python-Umgebung an einem laufenden Prozess auslesen:"
	echo "cat /proc/\\$(ps aux | egrep '(python|gunicorn)' | grep -v grep | head -n1 | awk '{ print \\$2 }')/environ | tr \\\\0 \\\\n"
	echo ""
	cf ssh $(PROJECT_SLUG)

{% if cookiecutter.use_docker.startswith('y') -%}
build-docker:
	docker build -t {{cookiecutter.docker_repository}}{{'/' if cookiecutter.docker_repository else ''}}{{cookiecutter.docker_project_name}}:{{cookiecutter.docker_default_tag}} .

build-and-push: build-docker
	docker push {{cookiecutter.docker_repository}}{{'/' if cookiecutter.docker_repository else ''}}{{cookiecutter.docker_project_name}}:{{cookiecutter.docker_default_tag}}

start-docker:
	docker rm "$(PROJECT_SLUG)" || true
	docker run --name "$(PROJECT_SLUG)" -p "127.0.0.1:{{cookiecutter.api_port}}:{{cookiecutter.api_port}}" {{cookiecutter.docker_repository}}{{'/' if cookiecutter.docker_repository else ''}}{{cookiecutter.docker_project_name}}:{{cookiecutter.docker_default_tag}}

attach-to-docker:
	 docker exec -i -t $(PROJECT_SLUG) /bin/bash 
{%- endif %}
