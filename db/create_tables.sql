drop table if exists user;
drop table if exists listing;
drop table if exists category;
drop table if exists listing_category;

create table user
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
  total_price        numeric(5,2)             not null,
  price_per_unit     numeric(5,2)             not null,
  listing_category   varchar(64)              not null,
  is_tradeable       boolean default false    not null,
  is_active          boolean default true     not null,
  date_created       timestamp with time zone not null,
  date_harvested     timestamp with time zone not null,
  date_modified      timestamp with time zone not null
);

create unique index listing_listing_id_uindex on listing (listing_id);
create unique index lower_title_idx on listing ((lower(title)));

create table category
(
  category_id serial      not null
    constraint category_pkey
    primary key,
  name        varchar(64) not null
);

create unique index category_category_id_uindex on category (category_id);
create unique index category_name_uindex on category (name);

create table listing_category
(
  listing_id  integer not null
    constraint listing_category_listing_listing_id_fk
    references listing,
  category_id integer not null
    constraint listing_category_category_category_id_fk
    references category,
  constraint listing_category_category_id_listing_id_pk
  primary key (category_id, listing_id)
);
