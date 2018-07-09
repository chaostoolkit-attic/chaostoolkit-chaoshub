#!/bin/bash
set -eo pipefail

function lint () {
    echo "Checking the code syntax"
    pycodestyle --first chaoshub
}

function build () {
    echo "Building the chaostoolkit-chaoshub package"
    python setup.py build
}

function release () {
    echo "Releasing the package"
    python setup.py release

    echo "Publishing to PyPI"
    pip install twine
    twine upload dist/* -u ${PYPI_USER_NAME} -p ${PYPI_PWD}
}

function main () {
    lint || return 1
    build || return 1

    if [[ $TRAVIS_PYTHON_VERSION =~ ^3\.5+$ ]]; then
        if [[ $TRAVIS_TAG =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Releasing tag $TRAVIS_TAG with Python $TRAVIS_PYTHON_VERSION"
            release || return 1
        fi
    fi
}

main "$@" || exit 1
exit 0
