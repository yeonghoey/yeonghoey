#!/usr/bin/env bash

set -euo pipefail

readonly REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

git -C "$REPO" pull --rebase --autostash
git -C "$REPO" lfs pull
