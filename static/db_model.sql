-- Active: 1695991712872@@127.0.0.1@3306@furina
create Table API_images(
   id int PRIMARY KEY,
   filename VARCHAR(255),
   userpicname VARCHAR(255)
)

create Table API_music(
   id int PRIMARY KEY,
   filename VARCHAR(255),
   usermusicname VARCHAR(255)
)

create table API_spider (
id int PRIMARY KEY,
videoname varchar(255) not null,
audioname varchar(255) not null,
bv_code varchar(255) not null
)