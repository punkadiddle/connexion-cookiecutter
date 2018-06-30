#!/bin/bash
BASE_DIR="${PWD}"
CHECKOUT_FOLDER='project-git'
VERSION="$(cat "${BASE_DIR}/version/version")"
source "${CHECKOUT_FOLDER}/ci/common/scripts/lib.sh"

export PIP_CACHE_DIR="${PWD}/pip-cache"
export PIPENV_CACHE_DIR="${PWD}/pip-cache"
export PIPENV_VENV_IN_PROJECT=1
export PIPENV_NOSPIN=1
export SETUPTOOLS_SCM_PRETEND_VERSION

# inject version since it is not published to git yet
SETUPTOOLS_SCM_PRETEND_VERSION=$(tr -d '-' <<< "${VERSION}")
echo -n "${VERSION}" > "${CHECKOUT_FOLDER}/.version"

# remove old artifacts from cache
find "${PIP_CACHE_DIR}" -mtime +10 -type f -delete && find "${PIP_CACHE_DIR}" -mindepth 1 -empty -type d -delete

echo "Testing ${VERSION}"

cd "${CHECKOUT_FOLDER}" || exit 1

if [[ -f "Pipfile" ]]; then
    header "Found Pipfile, using pipenv"
    python -m pip install pipenv || exit 1

    pipenv install --dev || exit 1

    pipenv run python setup.py test
    result=$?

else
    echo "No supported dependency artefact found!" >&2
    exit 1
fi
line

header "running pylint for SonarQube (pylint-report.txt)"
pipenv run pylint --output-format text --msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' src | tee pylint-report.txt
line

mv "${BASE_DIR}/${CHECKOUT_FOLDER}"/{,.[!.]}* "${BASE_DIR}/sonarqube-scanner-input/"
exit $result
