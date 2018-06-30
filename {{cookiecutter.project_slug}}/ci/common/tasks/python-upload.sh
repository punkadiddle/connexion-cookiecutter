#!/bin/bash
BASE_DIR="${PWD}"
CHECKOUT_DIR='project-git'
DIST_DIR='project-dist'
VERSION="$(cat "${BASE_DIR}/version/version")"
source "${CHECKOUT_DIR}/ci/common/scripts/lib.sh"

export PIP_CACHE_DIR="${PWD}/pip-cache"
export TWINE_REPOSITORY_URL
export TWINE_USERNAME
export TWINE_PASSWORD

python -m twine || exit 1

cd "$DIST_DIR"

dline "uploading"
while IFS=  read -r file -d $'\0'; do
    twine upload "${file}"
    result=$?
done < <(find "$DIST_DIR" -type f -name "${DIST_FILE_GLOB}" -print0)

exit $result
