-- user table
insert into public.user (user_id, address_id, username, password, first_name, last_name, profile_pic, bio) 
values (1, 1, 'hannes', 'hannes', 'hannes', 'widrig', 'https://avatars0.githubusercontent.com/u/3399497?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');
insert into public.user (user_id, address_id, username, password, first_name, last_name, profile_pic, bio) 
values (2, 1, 'amish', 'amish', 'amish', 'mishra', 'https://avatars0.githubusercontent.com/u/36204169?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');
insert into public.user (user_id, address_id, username, password, first_name, last_name, profile_pic, bio) 
values (3, 1, 'john', 'john', 'john', 'meharg', 'https://avatars2.githubusercontent.com/u/7091411?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');
insert into public.user (user_id, address_id, username, password, first_name, last_name, profile_pic, bio) 
values (4, 1, 'tim', 'tim', 'tim', 'ours', 'https://avatars2.githubusercontent.com/u/22141109?s=400&v=4', 'Lorem ipsum dolor sit amet, vix cu partem mollis, at mea reque accumsan. Mea novum nominavi accusamus no, utroque delicatissimi no sed. Quo te.');

-- listing table
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, is_tradeable, is_active, date_created, date_harvested, date_modified) 
values (1, 1, 'Peppers', 'https://fthmb.tqn.com/UXEQ2D6wEPKC9MyyTU-sk5Rcpx8=/960x0/filters:no_upscale():max_bytes(150000):strip_icc()/Peppers-Sweet-Mix-579bb8773df78c3276657310.jpg', 'peppers are almost gone in upland, in', 60, 50, 'dozen', 5.00, 1.00, 1, false, true, '2018-03-15 15:31:40.858000', '2018-03-12 15:31:46.176000', '2018-03-15 15:31:50.313000');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, is_tradeable, is_active, date_created, date_harvested, date_modified) 
values (2, 2, 'Zucchini', 'https://imagesvc.timeincapp.com/v3/mm/image?url=http%3A%2F%2Fcdn-img.health.com%2Fsites%2Fdefault%2Ffiles%2Fstyles%2Fmedium_16_9%2Fpublic%2Fstyles%2Fmain%2Fpublic%2Fgettyimages-126549235.jpg%3Fitok%3Dsi14dXXo&w=700&q=85', 'zucchini will be gone soon!', 12, 11, 'dozen', 132.00, 11.00, 1, false, true, '2018-04-05 03:50:45.590577', '2018-10-12 04:00:00.000000', '2018-04-05 03:50:45.590577');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, is_tradeable, is_active, date_created, date_harvested, date_modified) 
values (3, 3, 'Corn', 'https://fthmb.tqn.com/yFg2716G8Awd6XHALEJMwSJxMDI=/960x0/filters:no_upscale():max_bytes(150000):strip_icc()/fresh_corn-583dfbd65f9b58d5b170c933.jpg', 'corn going quickly in upland, in', 36, 19, 'dozen', 6.00, 2.00, 1, false, true, '2018-03-15 15:16:13.075000', '2018-03-12 15:16:19.369000', '2018-03-15 15:16:24.213000');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, is_tradeable, is_active, date_created, date_harvested, date_modified) 
values (4, 4, 'Tomatoes', 'https://thumbs-prod.si-cdn.com/6w-ayTNsYYXdnmN8jlJkG0pzEUA=/800x600/filters:no_upscale()/https://public-media.smithsonianmag.com/filer/44/de/44de0f61-47cb-4289-aaf0-73e71d39fefb/2962762666_1237ff6eb4_o.jpg', 'selling fast in upland, in', 15, 13, 'each', 10.00, 1.00, 1, false, true, '2018-03-15 15:14:21.402000', '2018-03-12 15:14:36.336000', '2018-03-15 15:14:47.469000');
insert into public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, is_tradeable, is_active, date_created, date_harvested, date_modified) 
values (5, 4, 'Cucumbers', 'http://cdn2.cocinadelirante.com/sites/default/files/styles/gallerie/public/images/2016/08/pepinos.jpg', 'cucumbers are almost gone in upland, in', 60, 12, 'dozen', 5.00, 1.00, 1, false, true, '2018-03-15 15:31:40.858000', '2018-03-12 15:31:46.176000', '2018-03-15 15:31:50.313000');
alter sequence listing_listing_id_seq restart with 6;

-- category table
insert into public.category (category_id, name) values (1, 'vegetable');
insert into public.category (category_id, name) values (2, 'fruit');
insert into public.category (category_id, name) values (3, 'meat');
insert into public.category (category_id, name) values (4, 'cheese');
alter sequence category_category_id_seq restart with 5;

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

insert into public.address (street, city, state_id, zipcode) values ('236 West Reade Ave', 'Upland', 15, '46989');