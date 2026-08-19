CREATE DATABASE IF NOT EXISTS woodytoys;
USE woodytoys;

CREATE TABLE IF NOT EXISTS products (
  id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  product_name VARCHAR(255),
  product_price VARCHAR(255),
  PRIMARY KEY (id)
);

INSERT INTO products (product_name, product_price)
VALUES ('Set de 100 cubes multicolores','50'),
       ('Yoyo','10'),
       ('Circuit de billes','75'),
       ('Arc a fleches','20'),
       ('Maison de poupees','150');
