CREATE USER app WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD 'app';
    
CREATE DATABASE app
    WITH 
    OWNER = app
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

create schema APP;
grant all privileges on schema APP to APP;

create table APP.S_RIGHTS
(
    RIGHT_ID varchar(50) not null,
    LABEL varchar(100) not null,
    primary key (RIGHT_ID)
);
grant all privileges on table APP.S_RIGHTS to APP;

create table APP.S_ROLES
(
    ROLE_ID varchar(50) not null,
    LABEL varchar(50) not null,
    primary key (ROLE_ID)
);
grant all privileges on table APP.S_ROLES to APP;

insert into APP.S_ROLES values ('ROLE_USER','User');
insert into APP.S_ROLES values ('ROLE_ADMIN','Admin');

create table APP.T_ROLES_RIGHTS
(
    ROLE_ID varchar(50) not null,
    RIGHT_ID varchar(50) not null,
    primary key (ROLE_ID, RIGHT_ID),
    foreign key (ROLE_ID) references APP.S_ROLES (ROLE_ID) on delete restrict,
    foreign key (RIGHT_ID) references APP.S_RIGHTS (RIGHT_ID) on delete restrict
);
grant all privileges on table APP.T_ROLES_RIGHTS to APP;

create table APP.T_ACCESS_TOKENS (
	ID varchar(16) not null,
	EXPIRY timestamp, 
	TOKEN varchar(255) not null, 
	USER_ID varchar(16) not null, 
	primary key (ID, TOKEN),
	foreign key (USER_ID) references APP.T_USER (ID) on delete restrict
);
grant all privileges on table APP.T_ACCESS_TOKENS to APP;

create table APP.T_USER (
	ID varchar(16) not null, 
	FORENAME varchar(50) not null, 
	PASSWORD varchar(80) not null, 
	SURNAME varchar(50) not null, 
	USERNAME varchar(50) not null unique, 
	primary key (ID)
);
grant all privileges on table APP.T_USER to APP;

insert into APP.T_USER values ('A7BU1ZBUgL','Thiago', '$2b$12$3BuLlTO02cb61trmjZOC4OikAq6v.C6tK9cwd0dz.osvRTgL0IrjO', 'Junqueira', 'admin');
insert into APP.T_USER values ('B7BU2ZBUgL','Julia', '$2b$12$3BuLlTO02cb61trmjZOC4OikAq6v.C6tK9cwd0dz.osvRTgL0IrjO', 'Sammler', 'july');

create table APP.T_USER_ROLES (
    USER_ID varchar(16) not null,
    ROLE_ID varchar(50) not null,
    LASTCHANGE_BY varchar(16),
    LASTCHANGE_AT timestamp,
    primary key (USER_ID, ROLE_ID),
    foreign key (USER_ID) references APP.T_USER (ID) on delete restrict,
    foreign key (ROLE_ID) references APP.S_ROLES (ROLE_ID) on delete restrict
);
grant all privileges on table APP.T_USER_ROLES to APP;

insert into APP.T_USER_ROLES values ('A7BU1ZBUgL','ROLE_ADMIN');
insert into APP.T_USER_ROLES values ('A7BU1ZBUgL','ROLE_USER');
insert into APP.T_USER_ROLES values ('B7BU2ZBUgL','ROLE_USER');

