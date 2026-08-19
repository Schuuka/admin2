#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-ttranthi}"
VERSION="${VERSION:-tp9}"

build_push () {
  local path="$1" name="$2"
  echo "==> $name"
  docker build -t "$NAMESPACE/$name:$VERSION" "$path"
  docker push "$NAMESPACE/$name:$VERSION"
}

cd "$(dirname "$0")"

build_push misc-service    woody9-misc
build_push product-service woody9-product
build_push order-service   woody9-order
build_push order-worker    woody9-order-worker
build_push reverse-proxy   woody9-reverse
build_push front           woody9-front

echo "OK - version poussee : $VERSION"
