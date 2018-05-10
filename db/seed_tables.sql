-- user table
insert into public.user (user_id, address_id, email, password, first_name, last_name, profile_pic, bio)
values (1, 1, 'hannes@widrig.com', 'hannes', 'hannes', 'widrig', 'https://avatars0.githubusercontent.com/u/3399497?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');
insert into public.user (user_id, address_id, email, password, first_name, last_name, profile_pic, bio)
values (2, 1, 'amish@mishra.edu', 'amish', 'amish', 'mishra', 'https://avatars0.githubusercontent.com/u/36204169?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');
insert into public.user (user_id, address_id, email, password, first_name, last_name, profile_pic, bio)
values (3, 1, 'jon@meharg.gov', 'jon', 'jon', 'meharg', 'https://avatars2.githubusercontent.com/u/7091411?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');
insert into public.user (user_id, address_id, email, password, first_name, last_name, profile_pic, bio)
values (4, 1, 'tim@ours.org', 'tim', 'tim', 'ours', 'https://avatars2.githubusercontent.com/u/22141109?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');
alter sequence user_user_id_seq restart with 5;

-- category table
insert into public.category (category_id, name) values (1, 'vegetable');
insert into public.category (category_id, name) values (2, 'fruit');
insert into public.category (category_id, name) values (3, 'meat');
insert into public.category (category_id, name) values (4, 'cheese');
alter sequence category_category_id_seq restart with 5;

-- listing table
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, category_id, is_tradeable, is_active, date_created, date_harvested, date_modified)
values (1, 1, 'Peppers', 'images/uploaded-images/Peppers.jpg', 'peppers are almost gone in upland, in', 60, 50, 'dozen', 5.00, 1.00, 1, false, true, '2018-03-15 15:31:40.858000', '2018-03-12 15:31:46.176000', '2018-03-15 15:31:50.313000');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, category_id, is_tradeable, is_active, date_created, date_harvested, date_modified)
values (2, 2, 'Zucchini', 'images/uploaded-images/Zucchini.jpg', 'zucchini will be gone soon!', 12, 11, 'dozen', 132.00, 11.00, 1, false, true, '2018-04-05 03:50:45.590577', '2018-10-12 04:00:00.000000', '2018-04-05 03:50:45.590577');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, category_id, is_tradeable, is_active, date_created, date_harvested, date_modified)
values (3, 3, 'Corn', 'images/uploaded-images/Corn.jpg', 'corn going quickly in upland, in', 36, 19, 'dozen', 6.00, 2.00, 1, false, true, '2018-03-15 15:16:13.075000', '2018-03-12 15:16:19.369000', '2018-03-15 15:16:24.213000');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, category_id, is_tradeable, is_active, date_created, date_harvested, date_modified)
values (4, 4, 'Tomatoes', 'images/uploaded-images/Tomatoes.jpg', 'selling fast in upland, in', 15, 13, 'each', 10.00, 1.00, 1, false, true, '2018-03-15 15:14:21.402000', '2018-03-12 15:14:36.336000', '2018-03-15 15:14:47.469000');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, category_id, is_tradeable, is_active, date_created, date_harvested, date_modified)
values (5, 4, 'Cucumbers', 'images/uploaded-images/Cucumbers.jpg', 'cucumbers are almost gone in upland, in', 60, 12, 'dozen', 5.00, 1.00, 1, false, true, '2018-03-15 15:31:40.858000', '2018-03-12 15:31:46.176000', '2018-03-15 15:31:50.313000');
alter sequence listing_listing_id_seq restart with 6;

-- state table
insert into public.state (abbrev, name) values
('AL', 'Alabama'),
('AK', 'Alaska'),
('AZ', 'Arizona'),
('AR', 'Arkansas'),
('CA', 'California'),
('CO', 'Colorado'),
('CT', 'Connecticut'),
('DE', 'Delaware'),
('DC', 'District of Columbia'),
('FL', 'Florida'),
('GA', 'Georgia'),
('HI', 'Hawaii'),
('ID', 'Idaho'),
('IL', 'Illinois'),
('IN', 'Indiana'),
('IA', 'Iowa'),
('KS', 'Kansas'),
('KY', 'Kentucky'),
('LA', 'Louisiana'),
('ME', 'Maine'),
('MD', 'Maryland'),
('MA', 'Massachusetts'),
('MI', 'Michigan'),
('MN', 'Minnesota'),
('MS', 'Mississippi'),
('MO', 'Missouri'),
('MT', 'Montana'),
('NE', 'Nebraska'),
('NV', 'Nevada'),
('NH', 'New Hampshire'),
('NJ', 'New Jersey'),
('NM', 'New Mexico'),
('NY', 'New York'),
('NC', 'North Carolina'),
('ND', 'North Dakota'),
('OH', 'Ohio'),
('OK', 'Oklahoma'),
('OR', 'Oregon'),
('PA', 'Pennsylvania'),
('PR', 'Puerto Rico'),
('RI', 'Rhode Island'),
('SC', 'South Carolina'),
('SD', 'South Dakota'),
('TN', 'Tennessee'),
('TX', 'Texas'),
('UT', 'Utah'),
('VT', 'Vermont'),
('VA', 'Virginia'),
('WA', 'Washington'),
('WV', 'West Virginia'),
('WI', 'Wisconsin'),
('WY', 'Wyoming');

-- address table
insert into public.address (street, city, state_id, zipcode) values ('236 West Reade Ave', 'Upland', 15, '46989');
alter sequence address_address_id_seq restart with 2;

-- orders table
insert into public.orders (listing_id, quantity, total_cost, buyer_id, time_placed) values (1, 10, 10.50, 2, '2018-05-05 11:31:46.000000');
insert into public.orders (listing_id, quantity, total_cost, buyer_id, time_placed) values (4, 112, 51.23, 2, '2018-05-06 11:31:46.000000');
insert into public.orders (listing_id, quantity, total_cost, buyer_id, time_placed) values (3, 24, 18.67, 1, '2018-05-07 11:31:46.000000');
insert into public.orders (listing_id, quantity, total_cost, buyer_id, time_placed) values (2, 1, 12.34, 3, '2018-05-08 11:31:46.000000');
insert into public.orders (listing_id, quantity, total_cost, buyer_id, time_placed) values (1, 12, 5.01, 4, '2018-05-09 11:31:46.000000');
alter sequence orders_order_id_seq restart with 6;