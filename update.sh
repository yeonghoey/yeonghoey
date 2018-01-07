#!/usr/bin/env bash

set -euo pipefail

readonly REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure lfs initialized
git lfs install --local

# NOTE: Smudging is much slower than 'git lfs pull'
GIT_LFS_SKIP_SMUDGE=1 \
  git -C "$REPO" pull --rebase --autostash
git -C "$REPO" lfs pull
