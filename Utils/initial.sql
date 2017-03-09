drop database if exists smonitor;
drop user if exists 'smonitor'@'localhost';
create user 'smonitor'@'localhost' identified by 'smonitor231#';
create database smonitor charset='utf8';
grant all privileges on smonitor.* to 'smonitor'@'localhost';
