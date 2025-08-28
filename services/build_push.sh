#!/usr/bin/env bash
set -euo pipefail

: "${REGISTRY:=docker.io}"
: "${NAMESPACE:=ttranthi}"
: "${VERSION:=v1}"

build_push () {
  local path="$1" name="$2"
  docker build -t "$REGISTRY/$NAMESPACE/$name:$VERSION" "$path"
  docker push "$REGISTRY/$NAMESPACE/$name:$VERSION"
}

build_push services/misc-service      woody-misc
build_push services/product-service   woody-product
build_push services/order-service     woody-order
build_push services/reverse-proxy    woody-reverse
build_push services/front            woody-front
build_push services/order-worker    woody-order-worker
# database utilise l'image officielle mariadb -> pas de build ici
echo "Done. Pushed version: $VERSION"
