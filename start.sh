#!/bin/bash

# Prompt user for MySQL username and password

#read -p "MySQL username: " username
#read -sp "MySQL password: " password
#echo
username="root"
password="1123581321"

# Prompt user for database name
#read -p "Database name: " dbname
dbname="Library"

# Delete database (Reset)
mysql -u "$username" -p"$password" -e "DROP DATABASE $dbname"
echo "Database Reset"

# Create database
mysql -u "$username" -p"$password" -e "CREATE DATABASE $dbname"
echo "Database Created"

# Create tables in the database

mysql -u "$username" -p"$password" "$dbname" << EOF
CREATE TABLE USER (
  user_id INT(6) UNSIGNED AUTO_INCREMENT,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL,
  address VARCHAR(30) NOT NULL,
  email VARCHAR(50),
  PRIMARY KEY (user_id)
);
EOF

mysql -u "$username" -p"$password" "$dbname" << EOF
CREATE TABLE LIBRARY_BOOK (
  book_id INT(6) UNSIGNED AUTO_INCREMENT,
  title VARCHAR(225) NOT NULL,
  author VARCHAR(225) NOT NULL,
  year_published INT(4),
  pages INT(5),
  borrowed_state VARCHAR(20) DEFAULT "Available",
  user_id INT(6) UNSIGNED DEFAULT NULL,
  PRIMARY KEY (book_id)
);
EOF

mysql -u "$username" -p"$password" "$dbname" << EOF
LOAD DATA INFILE '/var/lib/mysql-files/userData.csv' 
INTO TABLE USER
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
EOF

echo "Tables Created"
mysql -u "$username" -p"$password" "$dbname" << EOF
LOAD DATA INFILE '/var/lib/mysql-files/books.csv' 
INTO TABLE LIBRARY_BOOK
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
EOF


echo "Initial Load"



echo "Database and tables created successfully!"