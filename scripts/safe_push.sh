#!/usr/bin/env bash
set -euo pipefail

git fetch origin
git pull --rebase origin main
git push origin main
