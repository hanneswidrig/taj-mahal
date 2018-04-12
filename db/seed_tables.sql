-- User Table
INSERT INTO public.user (user_id, address_id, username, password, first_name, last_name, profile_pic, bio) 
VALUES (1, 1, 'hannes', 'hannes', 'Hannes', 'Widrig', 'https://avatars0.githubusercontent.com/u/3399497?s=400&v=4', 'From Alabama!');

-- Listing Table
INSERT INTO public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, listing_quality, is_tradeable, is_active, date_created, expiration_date, date_modified) 
VALUES (1, 2, 'Peppers', 'https://fthmb.tqn.com/UXEQ2D6wEPKC9MyyTU-sk5Rcpx8=/960x0/filters:no_upscale():max_bytes(150000):strip_icc()/Peppers-Sweet-Mix-579bb8773df78c3276657310.jpg', 'Peppers are almost gone in Upland, IN', 60, 50, 'dozen', 5.00, 1.00, 'vegetable', 'fresh', false, true, '2018-03-15 15:31:40.858000', '2018-03-21 15:31:46.176000', '2018-03-15 15:31:50.313000');
INSERT INTO public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, listing_quality, is_tradeable, is_active, date_created, expiration_date, date_modified) 
VALUES (2, 0, 'Zucchini', 'https://imagesvc.timeincapp.com/v3/mm/image?url=http%3A%2F%2Fcdn-img.health.com%2Fsites%2Fdefault%2Ffiles%2Fstyles%2Fmedium_16_9%2Fpublic%2Fstyles%2Fmain%2Fpublic%2Fgettyimages-126549235.jpg%3Fitok%3Dsi14dXXo&w=700&q=85', 'Zucchini will be gone soon!', 12, 11, 'dozen', 132.00, 11.00, 'vegetable', 'fresh', false, true, '2018-04-05 03:50:45.590577', '2018-10-30 04:00:00.000000', '2018-04-05 03:50:45.590577');
INSERT INTO public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, listing_quality, is_tradeable, is_active, date_created, expiration_date, date_modified) 
VALUES (3, 1, 'Corn', 'https://fthmb.tqn.com/yFg2716G8Awd6XHALEJMwSJxMDI=/960x0/filters:no_upscale():max_bytes(150000):strip_icc()/fresh_corn-583dfbd65f9b58d5b170c933.jpg', 'Corn going quickly in Upland, IN', 36, 19, 'dozen', 6.00, 2.00, 'vegetable', 'fresh', false, true, '2018-03-15 15:16:13.075000', '2018-03-20 15:16:19.369000', '2018-03-15 15:16:24.213000');
INSERT INTO public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, listing_quality, is_tradeable, is_active, date_created, expiration_date, date_modified) 
VALUES (4, 0, 'Tomatoes', 'https://thumbs-prod.si-cdn.com/6w-ayTNsYYXdnmN8jlJkG0pzEUA=/800x600/filters:no_upscale()/https://public-media.smithsonianmag.com/filer/44/de/44de0f61-47cb-4289-aaf0-73e71d39fefb/2962762666_1237ff6eb4_o.jpg', 'Selling fast in Upland, IN', 15, 13, 'each', 10.00, 1.00, 'vegetable', 'fresh', false, true, '2018-03-15 15:14:21.402000', '2018-03-22 15:14:36.336000', '2018-03-15 15:14:47.469000');
INSERT INTO public.listing (listing_id, seller_id, title, photo, description, original_quantity, available_quantity, unit_type, total_price, price_per_unit, listing_category, listing_quality, is_tradeable, is_active, date_created, expiration_date, date_modified) 
VALUES (5, 2, 'Cucumbers', 'http://cdn2.cocinadelirante.com/sites/default/files/styles/gallerie/public/images/2016/08/pepinos.jpg', 'Cucumbers are almost gone in Upland, IN', 60, 12, 'dozen', 5.00, 1.00, 'vegetable', 'fresh', false, true, '2018-03-15 15:31:40.858000', '2018-03-21 15:31:46.176000', '2018-03-15 15:31:50.313000');
ALTER SEQUENCE listing_listing_id_seq RESTART WITH 6;

-- Category Table
INSERT INTO public.category (category_id, name) VALUES (1, 'vegetable');
INSERT INTO public.category (category_id, name) VALUES (2, 'fruit');
INSERT INTO public.category (category_id, name) VALUES (3, 'meat');
INSERT INTO public.category (category_id, name) VALUES (4, 'cheese');
ALTER SEQUENCE category_category_id_seq RESTART WITH 5;