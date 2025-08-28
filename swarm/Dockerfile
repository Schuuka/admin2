FROM php:8.3-apache

COPY index.html /var/www/html/index.php
EXPOSE 80

# Ajout d'un healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
