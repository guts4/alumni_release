#create database mydatabase character set utf8mb4 collate utf8mb4_general_ci;

create user userid@localhost identified by '1111';
GRANT ALL PRIVILEGES ON *.* TO 'userid'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;