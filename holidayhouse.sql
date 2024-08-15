DROP database if exists holidayhouse;
CREATE database holidayhouse;
USE holidayhouse;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `employee`;
DROP TABLE IF EXISTS `admin`;
DROP TABLE IF EXISTS `staff`;
DROP TABLE IF EXISTS `house`;
DROP TABLE IF EXISTS `customer`;

-- ----------------------------
-- Table structure for user
-- ----------------------------  
CREATE TABLE `user`(
	`user_id` int NOT NULL AUTO_INCREMENT Unique Key,
    `username` varchar(45) DEFAULT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `user_type`  varchar(45) DEFAULT NULL,
    PRIMARY KEY(`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for employee
-- ----------------------------  
CREATE TABLE `employee`(
	`employee_id` int NOT NULL,
    `user_id` int DEFAULT NULL,
    `e_fName` varchar(255) NOT NULL,
    `e_Lname` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `phone_num` varchar(255) DEFAULT NULL, 
    `date_joined` DATE DEFAULT NULL,
    `employee_role`  varchar(45) NOT NULL,
    PRIMARY KEY(`employee_id`),
    CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for admin
-- ----------------------------
CREATE TABLE `admin`(
	`admin_id` int NOT NULL,
    `employee_id` int DEFAULT NULL,
    `user_id` int DEFAULT NULL,
    `a_fName` varchar(45) NOT NULL,
    `a_Lname` varchar(45) NOT NULL,
    `email` varchar(255) NOT NULL,
    `phone_number` varchar(45) DEFAULT NULL,
    `date_joined`  DATE DEFAULT NULL,
    PRIMARY KEY(`admin_id`),
	KEY `employee` (`employee_id`),
    KEY `user` (`user_id`),
	CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`),
    CONSTRAINT `admin_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for staff
-- ----------------------------
CREATE TABLE `staff`(
	`staff_id` int NOT NULL AUTO_INCREMENT,
	`employee_id`int DEFAULT NULL,
    `user_id` int DEFAULT NULL,
    `s_fName` varchar(45) NOT NULL,
    `s_Lname` varchar(45) NOT NULL,
    `email` varchar(255) NOT NULL,
    `phone_number` varchar(45) DEFAULT NULL,
    `date_joined`  DATE DEFAULT NULL,
    PRIMARY KEY(`staff_id`),
    CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`),
    CONSTRAINT `staff_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    
    
-- ----------------------------
-- Table structure for house
-- ----------------------------    
CREATE TABLE `house`(
	`house_id` int NOT NULL AUTO_INCREMENT Unique Key,
    `h_address` varchar(225) NOT NULL,
    `bedroom_num` int NOT NULL,
    `bathroom_num` int NOT NULL,
    `max_occupancy` int NOT NULL,
    `rental_per_night` varchar(45) NOT NULL,
    `house_image`  VARCHAR(20) NOT NULL,
    `house_title` varchar(255) DEFAULT NULL,
	`house_description` text DEFAULT NULL,
    PRIMARY KEY(`house_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ----------------------------
-- Table structure for customer
-- ----------------------------
CREATE TABLE `customer`(
	`customer_id` int NOT NULL AUTO_INCREMENT Unique Key,
    `house_id` int DEFAULT NULL,
    `user_id` int DEFAULT NULL,
    `c_fName` varchar(45) DEFAULT NULL,
    `c_Lname` varchar(45) DEFAULT NULL,
    `address` varchar(45) DEFAULT NULL,
    `email` varchar(255) NOT NULL,
    `phone_num` varchar(45) DEFAULT NULL,
    PRIMARY KEY(`customer_id`),
    KEY `house` (`house_id`),
    KEY `user` (`user_id`),
	CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `house` (`house_id`),
    CONSTRAINT `customer_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/* ----- Insert data into the tables: ----- */
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3301,'123 Sunshine Blvd',3,2,7,'200','house1.jpg','Seaside Serenity Retreat','Embrace coastal living in this charming 3-bedroom beachfront cottage. Wake up to the sound of waves and enjoy breathtaking sunsets from your private patio.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3302,'456 Ocean View Dr',4,3,8,'250','house2.jpg','Mountain Paradise Hideaway','Nestled in the heart of the mountains, this cozy cabin offers a tranquil escape. Unwind by the fireplace or explore nearby hiking trails for the perfect nature retreat.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3303,'789 Mountain Retreat',4,2,6,'200','house3.jpg','Urban Oasis in the City Center','Experience the best of city living in this modern downtown apartment. Walk to trendy cafes, museums, and shops, and return to a stylish and comfortable home.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3304,'101 Elm Ln',3,2,5,'180','house4.jpg','Historic Charm in the Countryside','Step back in time with a stay in this beautifully restored farmhouse. Enjoy the peace of the countryside while surrounded by historical architecture and modern amenities.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3305,'202 Cedar Rd',3,1,3,'120','house5.jpg','Family-Friendly Lake House','Perfect for families, this spacious lakefront home features a private dock, kayaks, and a large yard for outdoor games. Create lasting memories in this idyllic setting.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3306,'303 Birch Dr',3,2,4,'130','house6.jpg','Ski-In/Ski-Out Chalet','Calling all winter enthusiasts! This ski-in/ski-out chalet offers direct access to the slopes, a cozy fireplace, and stunning mountain views. The ultimate winter wonderland getaway.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3307,'404 Maple Ct',4,2,6,'200','house7.jpg','Luxury Villa with Panoramic Views','Indulge in luxury in this exquisite villa perched on a hilltop. Enjoy sweeping views of the ocean, a private pool, and opulent interiors for a truly upscale experience.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3308,'505 Walnut Way',2,1,4,'140','house8.jpg','Romantic Cottage for Two','Escape to a romantic haven in this intimate cottage designed for couples. Relax in the hot tub, share a glass of wine by the fire, and savor the tranquility of your private retreat.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3309,'606 Spruce Ave',2,1,3,'130','house9.jpg','Rustic Log Cabin in the Woods','Immerse yourself in nature with a stay in this rustic log cabin surrounded by towering trees. Disconnect from the hustle and bustle and reconnect with the great outdoors.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3310,'707 Pinecrest Ln',5,2,7,'220','house10.jpg','Architectural Gem in the Desert','Discover a unique desert escape in this architecturally stunning home. With minimalist design, a pool, and desert views, it is the perfect blend of luxury and nature.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3311,'808 Redwood St',2,2,4,'120','house11.jpg','Hillside Haven with City Lights','Perched on a hillside, this stylish home offers panoramic views of the city lights below. Relax on the terrace, take a dip in the pool, and unwind in this modern retreat.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3312,'909 Magnolia Dr',3,1,4,'140','house12.jpg','Eco-Friendly Retreat by the River','Stay in harmony with nature in this eco-friendly retreat along the river. Solar panels, sustainable materials, and a peaceful environment make it an ideal green getaway.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3313,'111 Oakwood Cir',3,2,5,'180','house13.jpg','Historical Loft in the Arts District','Immerse yourself in culture with a stay in this historic loft located in the vibrant arts district. Walk to galleries, theaters, and eclectic cafes, and return to a stylish loft with character.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3314,'222 Cedarcrest Rd',2,1,3,'120','house14.jpg','Sunny Mediterranean Villa','Transport yourself to the Mediterranean with a stay in this sun-soaked villa. Enjoy al fresco dining, a private garden, and easy access to the beach for the perfect summer escape.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3315,'333 Birchwood Ln',2,1,4,'140','house15.jpg','Quaint Cottage with Vineyard Views','Experience wine country living in this charming cottage surrounded by vineyards. Sip local wines on the porch and soak in the beauty of the rolling hills.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3316,'444 Mapleton Ave',2,1,3,'120','house16.jpg','Treehouse Adventure for the Family','Give your family a unique experience in this treehouse surrounded by nature. With playful decor, a zip line, and treetop views, it is a magical retreat for all ages.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3317,'555 Sycamore Dr',3,2,4,'150','house17.jpg','Serenity on the Lakeside','Escape to tranquility with a stay in this lakeside retreat. Enjoy fishing, boating, and stargazing from the deck of this peaceful and secluded cabin.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3318,'666 Pinehurst Blvd',2,2,4,'160','house18.jpg','Asian-inspired Zen Retreat','Find your inner peace in this Zen-inspired retreat. With Japanese gardens, meditation spaces, and minimalist design, it is a perfect sanctuary for relaxation.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3319,'777 Elmwood Way',4,2,5,'180','house19.jpg','Surfers Paradise Beach House','Live the surfer s dream in this beachfront haven. With direct access to the waves, outdoor showers, and a laid-back vibe, it is a paradise for beach lovers.');
INSERT INTO `house` (`house_id`,`h_address`,`bedroom_num`,`bathroom_num`,`max_occupancy`,`rental_per_night`,`house_image`,`house_title`,`house_description`) VALUES (3320,'888 Oakridge Rd',4,2,6,'200','house20.jpg','Cozy Countryside Bungalow','Experience the simple joys of country living in this cozy bungalow. With a fireplace, rocking chairs on the porch, and views of rolling hills, it is the perfect escape from the city hustle.');
SELECT * FROM house;

INSERT INTO `customer` (`customer_id`,`house_id`,`user_id`,`c_fName`,`c_Lname`,`address`,`email`,`phone_num`) VALUES (1001,3303,1,'Alice','Moore','23 Main St, Cityville','alice@email.com','555-1234');
INSERT INTO `customer` (`customer_id`,`house_id`,`user_id`,`c_fName`,`c_Lname`,`address`,`email`,`phone_num`) VALUES (1002,3311,2,'Bob','Taylor','456 Oak Ave, Townburg','bob@email.com','555-5678');
INSERT INTO `customer` (`customer_id`,`house_id`,`user_id`,`c_fName`,`c_Lname`,`address`,`email`,`phone_num`) VALUES (1003,3318,3,'Charlie','Lee','789 Pine Rd, Villagetown','charlie@email.com','555-9876');
INSERT INTO `customer` (`customer_id`,`house_id`,`user_id`,`c_fName`,`c_Lname`,`address`,`email`,`phone_num`) VALUES (1004,3309,4,'David','Harris','321 Elm Blvd, Hamletville','david@email.com','555-4321');
INSERT INTO `customer` (`customer_id`,`house_id`,`user_id`,`c_fName`,`c_Lname`,`address`,`email`,`phone_num`) VALUES (1005,3320,5,'Emily','Clark','654 Birch Ln, Countryside','emily@email.com','555-8765');
SELECT * FROM customer;

INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (1,'Alice','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','alice@email.com','customer');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (2,'Bob','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','bob@email.com','customer');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (3,'Charlie','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','charlie@email.com','customer');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (4,'David','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','david@email.com','customer');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (5,'Emily','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','emily@email.com','customer');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (6,'Jennifer','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','jennifer@email.com','staff');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (7,'Michael','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','michael@example.com','staff');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (8,'Olivia','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','olivia@emailprovider.com','staff');
INSERT INTO `user`(`user_id`,`username`,`password`,`email`,`user_type`) VALUES (9,'Arlette','$2b$12$o8TpbnlfJYAl3jZoUPeAeu049zP2QD9g39gEUtR.pKCsgClSaxieK','arlette@email.com','admin');
SELECT * FROM user;

INSERT INTO `employee` (`employee_id`,`user_id`,`e_fName`,`e_Lname`,`email`,`phone_num`,`date_joined`,`employee_role`) VALUES (16801,6,'Jennifer',' Smith','jennifer@email.com','555-1234','2022-01-15','staff'); 
INSERT INTO `employee` (`employee_id`,`user_id`,`e_fName`,`e_Lname`,`email`,`phone_num`,`date_joined`,`employee_role`) VALUES (16802,7,'Michael','Brown','michael@example.com','555-5678','2022-02-20','staff'); 
INSERT INTO `employee` (`employee_id`,`user_id`,`e_fName`,`e_Lname`,`email`,`phone_num`,`date_joined`,`employee_role`) VALUES (16803,8,'Olivia','Wilson','olivia@emailprovider.com','555-9876','2021-03-10','staff');
INSERT INTO `employee` (`employee_id`,`user_id`,`e_fName`,`e_Lname`,`email`,`phone_num`,`date_joined`,`employee_role`) VALUES (16804,9,'Arlette','Miller','arlette@email.com','123-456-1111','2020-05-16','admin');
SELECT * FROM employee;

INSERT INTO `staff` (`staff_id`,`employee_id`,`user_id`,`s_fName`,`s_Lname`,`email`,`phone_number`,`date_joined`) VALUES (8001,16801,6,'Jennifer','Smith','jennifer@email.com','123-456-7890','2022-01-15');
INSERT INTO `staff` (`staff_id`,`employee_id`,`user_id`,`s_fName`,`s_Lname`,`email`,`phone_number`,`date_joined`) VALUES (8002,16802,7,'Michael','Brown','michael@example.com','987-654-3210','2021-02-20');
INSERT INTO `staff` (`staff_id`,`employee_id`,`user_id`,`s_fName`,`s_Lname`,`email`,`phone_number`,`date_joined`) VALUES (8003,16803,8,'Olivia','Wilson','olivia@emailprovider.com','555-123-4567','2022-03-10');
SELECT * FROM staff;

INSERT INTO `admin` (`admin_id`,`employee_id`,`user_id`,`a_fName`,`a_Lname`,`email`,`phone_number`,`date_joined`) VALUES (9001,16804,9,'Arlette','Miller','arlette@email.com','123-456-1111','2020-05-16');
SELECT * FROM admin;


SET FOREIGN_KEY_CHECKS = 1;
 
    