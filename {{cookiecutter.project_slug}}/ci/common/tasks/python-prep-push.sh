#!/bin/bash
BASE_DIR="${PWD}"
CHECKOUT_DIR='project-git'
VERSION="$(cat "${BASE_DIR}/version/version")"
source "${CHECKOUT_DIR}/ci/common/scripts/lib.sh"

echo "$VERSION" > "${CHECKOUT_DIR}/.version"

ls -al "${CHECKOUT_DIR}"

exit 0
