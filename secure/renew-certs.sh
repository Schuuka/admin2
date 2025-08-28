#!/bin/bash
cd ~/secure
docker compose exec -T web certbot renew --quiet
docker compose exec -T web nginx -s reload
