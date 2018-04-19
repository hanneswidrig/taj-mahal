drop table if exists "user" cascade;
drop table if exists listing cascade;
drop table if exists category cascade;
drop table if exists "state" cascade;
drop table if exists "address" cascade;

create table "user"
(
  user_id     serial      not null
    constraint user_pkey
    primary key,
  address_id  integer     not null,
  username    varchar(64) not null,
  password    varchar(64) not null,
  first_name  varchar(64) not null,
  last_name   varchar(64) not null,
  profile_pic varchar(256),
  bio         varchar(256)
);

create unique index user_user_id_uindex on "user" (user_id);
create unique index user_username_uindex on "user" (username);

create table category
(
  category_id serial      not null
    constraint category_pkey
    primary key,
  name        varchar(64) not null
);

create unique index category_category_id_uindex on category (category_id);
create unique index category_name_uindex on category (name);

create table "state"
(
  state_id serial      not null
    constraint state_pkey
    primary key,
  abbrev   varchar(2)  not null,
  name     varchar(32) not null
);

create unique index state_state_id_uindex on "state" (state_id);

create table listing
(
  listing_id         serial                   not null
    constraint listing_pkey
    primary key,
  seller_id          integer                  not null,
  title              varchar(128)             not null,
  photo              varchar(256)             not null,
  description        varchar(256)             not null,
  original_quantity  integer                  not null,
  available_quantity integer                  not null,
  unit_type          varchar(64)              not null,
  total_price        numeric(5, 2)            not null,
  price_per_unit     numeric(5, 2)            not null,
  category_id        integer                  not null
		constraint listing_category_category_id_fk
    references category,
  is_tradeable       boolean default false    not null,
  is_active          boolean default true     not null,
  date_created       timestamp with time zone not null,
  date_harvested     timestamp with time zone not null,
  date_modified      timestamp with time zone not null
);

create unique index listing_listing_id_uindex on listing (listing_id);
create unique index lower_title_idx on listing (lower(title :: text));

create table "address"
(
  address_id serial       not null
    constraint address_pkey
    primary key,
  street     varchar(128) not null,
  city       varchar(128) not null,
  state_id   integer      not null
    constraint address_state_state_id_fk
    references "state",
  zipcode    varchar(10)  not null
);

create unique index address_address_id_uindex on "address" (address_id);