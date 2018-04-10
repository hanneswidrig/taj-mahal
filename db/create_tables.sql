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
  total_price        numeric(5,2)               not null,
  price_per_unit     numeric(5,2)               not null,
  listing_category   varchar(64)              not null,
  listing_quality    varchar(64)              not null,
  is_tradeable       boolean default false    not null,
  is_active          boolean default true     not null,
  date_created       timestamp with time zone not null,
  expiration_date    timestamp with time zone not null,
  date_modified      timestamp with time zone not null
);

create unique index listing_listing_id_uindex
  on listing (listing_id);

create unique index lower_title_idx on listing ((lower(title)));


CREATE TABLE category
(
  category_id SERIAL      NOT NULL
    CONSTRAINT category_pkey
    PRIMARY KEY,
  name        VARCHAR(64) NOT NULL
);

CREATE UNIQUE INDEX category_category_id_uindex
  ON category (category_id);

CREATE UNIQUE INDEX category_name_uindex
  ON category (name);


CREATE TABLE listing_category
(
  listing_id  INTEGER NOT NULL
    CONSTRAINT listing_category_listing_listing_id_fk
    REFERENCES listing,
  category_id INTEGER NOT NULL
    CONSTRAINT listing_category_category_category_id_fk
    REFERENCES category,
  CONSTRAINT listing_category_category_id_listing_id_pk
  PRIMARY KEY (category_id, listing_id)
);
