drop table if exists "user";
drop table if exists "listing";


CREATE TABLE "user"
(
  user_id     SERIAL      NOT NULL
    CONSTRAINT user_pkey
    PRIMARY KEY,
  address_id  INTEGER     NOT NULL,
  username    VARCHAR(64) NOT NULL,
  password    VARCHAR(64) NOT NULL,
  first_name  VARCHAR(64) NOT NULL,
  last_name   VARCHAR(64) NOT NULL,
  profile_pic VARCHAR(256),
  bio         VARCHAR(256)
);

CREATE UNIQUE INDEX user_user_id_uindex
  ON "user" (user_id);

CREATE UNIQUE INDEX user_username_uindex
  ON "user" (username);


CREATE TABLE listing
(
  listing_id         SERIAL                   NOT NULL
    CONSTRAINT listing_pkey
    PRIMARY KEY,
  seller_id          INTEGER                  NOT NULL
    CONSTRAINT listing_seller_id_user_user_id___fk
    REFERENCES "user",
  title              VARCHAR(128)             NOT NULL,
  photo              VARCHAR(256)             NOT NULL,
  description        VARCHAR(256)             NOT NULL,
  original_quantity  INTEGER                  NOT NULL,
  available_quantity INTEGER                  NOT NULL,
  unit_type          VARCHAR(64)              NOT NULL,
  total_price        NUMERIC(5, 2)            NOT NULL,
  price_per_unit     NUMERIC(5, 2)            NOT NULL,
  listing_category   VARCHAR(64)              NOT NULL,
  listing_quality    VARCHAR(64)              NOT NULL,
  is_tradeable       BOOLEAN DEFAULT FALSE    NOT NULL,
  is_active          BOOLEAN DEFAULT TRUE     NOT NULL,
  date_created       TIMESTAMP WITH TIME ZONE NOT NULL,
  expiration_date    TIMESTAMP WITH TIME ZONE NOT NULL,
  date_modified      TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE UNIQUE INDEX listing_listing_id_uindex
  ON listing (listing_id);

create unique index lower_title_idx on listing ((lower(title)));