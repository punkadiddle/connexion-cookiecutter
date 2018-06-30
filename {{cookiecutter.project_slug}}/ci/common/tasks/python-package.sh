#!/bin/bash
BASE_DIR="${PWD}"
CHECKOUT_FOLDER='project-git'
DIST_DIR='project-dist'
VERSION="$(cat "${BASE_DIR}/version/version")"
source "${CHECKOUT_FOLDER}/ci/common/scripts/lib.sh"

export PIP_CACHE_DIR="${PWD}/pip-cache"
#export PIPENV_CACHE_DIR="${PWD}/pip-cache"
#export PIPENV_VENV_IN_PROJECT=1
#export PIPENV_NOSPIN=1
export SETUPTOOLS_SCM_PRETEND_VERSION

# inject version since it is not published to git yet
SETUPTOOLS_SCM_PRETEND_VERSION=$(tr -d '-' <<< "${VERSION}")

cd "${CHECKOUT_FOLDER}" || exit 1

python -m pip install setuptools wheel || exit 1

# if [[ -f "Pipfile" ]]; then
#     header "Found Pipfile, using pipenv"
#     python -m pip install pipenv || exit 1

#     pipenv install --dev || exit 1

#     pipenv run python setup.py test
#     result=$?

# else
#     echo "No supported dependency artefact found!" >&2
#     exit 1
# fi
dline "packaging"
python setup.py bdist sdist --dist-dir "${DIST_DIR}"
result=$?
line

ls -al "${DIST_DIR}"

exit $result
