#!/usr/bin/env bash

set -euo pipefail

pip install pipenv

readonly PANDOC_VERSION='2.2.1'
readonly PANDOC_DEB="pandoc-${PANDOC_VERSION}-1-amd64.deb"
readonly PANDOC_URL="https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/${PANDOC_DEB}"

wget "${PANDOC_URL}"
dpkg -i "${PANDOC_DEB}"
