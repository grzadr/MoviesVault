#! /bin/bash

set -eux
set -o pipefail

docker-compose build --force-rm --no-cache

