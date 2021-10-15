DROP DATABASE IF EXISTS  `hotel_reservation`;
CREATE DATABASE IF NOT EXISTS `hotel_reservation`;
USE `hotel_reservation`;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS user;

CREATE TABLE user (
  user_id int NOT NULL AUTO_INCREMENT,
  first_name char(50) NOT NULL,
  last_name char(50) NOT NULL,
  email varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  isAdmin boolean DEFAULT FALSE,
  phone_number char(15) DEFAULT NULL,
  date_of_birth date NOT NULL,
  PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting data into user table 

INSERT INTO `hotel_reservation`.`user` 
(`first_name`,
`last_name`,
`date_of_birth`,
`phone_number`,
`email`,
`password`,
`isAdmin`
)
 VALUES 
 ('Babara','MacCaffrey','1986-03-28','781-932-9754','barbara.Mac@gmail.com','1234',default ), 
 ('Ines','Brushfield','1986-04-13','804-427-9456','ines.b@yahoo.com', '54321',default),
 ('Freddi','Boagey','1985-02-07','719-724-7869','freddi.b@gmail.com','qwe123', default),
 ('Ambur','Roseburgh','1974-04-14','407-231-8017','ambur.r@gmail.com','123456', true),
 ('Clemmie','Betchley','1973-11-07',NULL,'clemmie.b@gmail.com','asd123',default);


--
-- Table structure for table `hotel`
--

DROP TABLE IF EXISTS `hotel`;

CREATE TABLE `hotel` (
  `hotel_id` int NOT NULL AUTO_INCREMENT,
  `street_address` varchar(50) NOT NULL,
  `city` char(25) NOT NULL,
  `state` char(2) NOT NULL,
  `zipcode` int NOT NULL,
  `number_of_rooms` INT NOT NULL,
  `phone_number` char(15) NOT NULL,
  `hotel_name` varchar(50) NOT NULL,
  `weekend_diff_percentage` decimal(3,2),
  PRIMARY KEY (`hotel_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting data into hotel table 

INSERT INTO `hotel_reservation`.`hotel` 
(
`hotel_name`,
`street_address`,
`city`,
`state`,
`zipcode`,
`number_of_rooms`,
`phone_number`,
`weekend_diff_percentage`
)
 VALUES 
 ('The Magnolia All Suites','14187 Commercial Trail','Hampton','VA',23452, 20, '213-342-5433', 0.25),
 ('The Lofts at Town Centre','251 Springs Junction','Colorado Springs','CO', 54789, 60, '532-543-7970', 0.35),
 ('Park North Hotel','30 Arapahoe Terrace','Orlando','FL',75231, 100, '854-324-7653', 0.15),
 ('The Courtyard Suites','5 Spohn Circle','Arlington','TX',78532, 20, '747-231-8017', 0.25),
 ('The Regency Rooms','7 Manley Drive','Chicago','IL', 54932, 20, '876-462-1211', 0.25),
 ('Town Inn Budget Rooms','50 Lillian Crossing','Nashville','TN', 68423, 150, '210-435-3422', 0.15),
 ('The Comfy Motel Place','538 Mosinee Center','Sarasota','FL', 75765, 50, '854-899-4532', 0.10),
 ('Sun Palace Inn','3520 Ohio Trail','Visalia','CA', 97453, 50, '634-112-6543', 0.25),
 ('HomeAway Inn','68 Lawn Avenue','Atlanta','GA', 43832, 30, '774-332-9943', 0.25),
 ('Rio Inn','123 Avenue','Austin','TX', 78352, 50, '210-342-9943', 0.20);


--
-- Table structure for table `amenities`
--

DROP TABLE IF EXISTS `amenities`;

CREATE TABLE `amenities` (
  `amenity_id` int NOT NULL AUTO_INCREMENT,
  `amenity_name` char(70) NOT NULL,
  PRIMARY KEY (`amenity_id`),
  UNIQUE KEY `amenity_name_UNIQUE` (`amenity_name`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Insert data into amenities table
INSERT INTO `hotel_reservation`. `amenities`
(`amenity_name`) VALUES ('Pool'), ('Gym'), ('Buiness office'), ('Spa');

--
-- Table structure for table `hotel_amenities`
--

DROP TABLE IF EXISTS `hotel_amenities`;

CREATE TABLE `hotel_amenities` (
  `hotel_id` int NOT NULL,
  `amenity_id` int NOT NULL,
  PRIMARY KEY (`hotel_id`,`amenity_id`),

  CONSTRAINT `hotel_amenities_amenity_id_fk` 
  FOREIGN KEY (`amenity_id`) 
  REFERENCES `amenities` (`amenity_id`) 
  ON DELETE CASCADE 
  ON UPDATE CASCADE,

  CONSTRAINT `hotel_amenities_hotel_id_fk` 
  FOREIGN KEY (`hotel_id`) 
  REFERENCES `hotel` (`hotel_id`) 
  ON DELETE CASCADE 
  ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert data into hotel_amenities
INSERT INTO `hotel_reservation`. `hotel_amenities` (`hotel_id`, `amenity_id`) 
VALUES 
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 1), (2, 2), (2, 3),
(3, 1), (3, 2), 
(4, 1), (4, 2), (4, 3), (4, 4), 
(5, 1), (5, 2), (5, 3), (5, 4),
(6, 1),
(8, 1), (8, 2), 
(9, 1), (9, 3), 
(10, 1);

--
-- Table structure for table `room_type`
--

DROP TABLE IF EXISTS `room_type`;

CREATE TABLE `room_type` (
  `room_type_id` int NOT NULL AUTO_INCREMENT,
  `room_type_name` varchar(128) NOT NULL,
  PRIMARY KEY (`room_type_id`),
  UNIQUE KEY `room_type_name_UNIQUE` (`room_type_name`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert data into room_type table
INSERT INTO `hotel_reservation`. `room_type`
(`room_type_name`) 
VALUES 
('Standard'), ('Queen'), ('King');


--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `hotel_room_type`;

CREATE TABLE `hotel_room_type` (
  `room_type_id` int NOT NULL,
  `hotel_id` int NOT NULL,
  `room_type_count` int NOT NULL,
  `price_per_night` decimal(10,2) NOT NULL,
  PRIMARY KEY (`room_type_id`, `hotel_id`),

  CONSTRAINT `hotel_id_fk` 
  FOREIGN KEY (`hotel_id`) 
  REFERENCES `hotel` (`hotel_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE,

  CONSTRAINT `hotel_room_type_id_fk`
  FOREIGN KEY (`room_type_id`) 
  REFERENCES `room_type` (`room_type_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `hotel_reservation`. `hotel_room_type` 
(`hotel_id`, `room_type_id`, `room_type_count`,  `price_per_night`) 
VALUES 
(1, 1, 10, 100),
(1, 2, 5, 150),
(1, 3, 5, 250),
(2, 1, 30, 105),
(2, 2, 20, 120),
(2, 3, 10, 190),
(3, 1, 50, 50),
(3, 2, 25, 75),
(3, 3, 25, 90),
(4, 1, 10, 100),
(4, 2, 5, 150),
(4, 3, 5, 250),
(5, 1, 15, 100),
(5, 2, 3, 150),
(5, 3, 2, 250),
(6, 1, 75, 25),
(6, 2, 50, 50),
(6, 3, 25, 60),
(7, 1, 25, 30),
(7, 2, 25, 50),
(8, 1, 25, 40),
(8, 2, 15, 60),
(8, 3, 10, 80),
(9, 1, 30, 50),
(10, 1, 25, 25),
(10, 2, 18, 55),
(10, 3, 7, 89);
--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;

CREATE TABLE `reservations` (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `hotel_id` int NOT NULL,
  `check_in` date NOT NULL,
  `check_out` date NOT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `status` tinytext DEFAULT NULL,
  PRIMARY KEY (`reservation_id`),

  CONSTRAINT `reservations_user_id_fk`
  FOREIGN KEY (`user_id`)
  REFERENCES `user` (`user_id`),
  
  CONSTRAINT `reservations_hotel_id_fk`
  FOREIGN KEY (`hotel_id`)
  REFERENCES `hotel` (`hotel_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Table structure for table `room_reserved`
--

DROP TABLE IF EXISTS `room_type_reserved`;

CREATE TABLE `reserved_room_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reservation_id` int NOT NULL,
  `room_type_id` int NOT NULL,
  PRIMARY KEY (`id`),

  CONSTRAINT `reservation_id_fk` 
  FOREIGN KEY (`reservation_id`) 
  REFERENCES `reservations` (`reservation_id`) 
  ON DELETE CASCADE ON UPDATE CASCADE, 

  CONSTRAINT `reserved_room_type_id_fk`
  FOREIGN KEY (`room_type_id`)
  REFERENCES `room_type` (`room_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;