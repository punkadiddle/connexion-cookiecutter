#!/bin/bash
BASE_DIR="${PWD}"
CHECKOUT_DIR='project-git'
VERSION="$(cat "${BASE_DIR}/version/version")"
source "${CHECKOUT_DIR}/ci/common/scripts/lib.sh"

export PIP_CACHE_DIR="${PWD}/pip-cache"
export SETUPTOOLS_SCM_PRETEND_VERSION

# inject version since it is not published to git yet
SETUPTOOLS_SCM_PRETEND_VERSION=$(tr -d '-' <<< "${VERSION}")
echo "$VERSION" > "${CHECKOUT_DIR}/.version"

cd "${CHECKOUT_DIR}" || exit 1

python -m pip install setuptools wheel || exit 1
python setup.py egg_info
result=$?

#pkgRoot="$(find "${CHECKOUT_DIR}/src/" -maxdepth 2 -type f -name '__init__.py' | head -n 1)"
#if [[ $? -eq 0 ]]; then
#    echo "$VERSION" >  "$(dirname "$pkgRoot")/.version"
#fi

mv "${BASE_DIR}/${CHECKOUT_FOLDER}"/{,.[!.]}* "${BASE_DIR}/project-dist/"
exit 0
