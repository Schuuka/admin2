-- L'utilisateur applicatif est cree par l'entrypoint MariaDB
-- (MARIADB_USER / MARIADB_PASSWORD_FILE) avec tous les droits sur la base.
-- On les reduit ici au strict necessaire : product-service ne fait que des SELECT.
REVOKE ALL PRIVILEGES ON woodytoys.* FROM 'woody-app'@'%';
GRANT SELECT ON woodytoys.* TO 'woody-app'@'%';
FLUSH PRIVILEGES;
