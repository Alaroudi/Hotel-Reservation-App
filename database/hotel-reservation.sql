DROP DATABASE IF EXISTS `hotel_reservation`;

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
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Inserting data into user table 
INSERT INTO
  `hotel_reservation`.`user` (
    `first_name`,
    `last_name`,
    `date_of_birth`,
    `phone_number`,
    `email`,
    `password`,
    `isAdmin`
  )
VALUES
  (
    'Babara',
    'MacCaffrey',
    '1986-03-28',
    '781-932-9754',
    'barbara.Mac@gmail.com',
    '1234',
    default
  ),
  (
    'Ines',
    'Brushfield',
    '1986-04-13',
    '804-427-9456',
    'ines.b@yahoo.com',
    '54321',
    default
  ),
  (
    'Freddi',
    'Boagey',
    '1985-02-07',
    '719-724-7869',
    'freddi.b@gmail.com',
    'qwe123',
    default
  ),
  (
    'Ambur',
    'Roseburgh',
    '1974-04-14',
    '407-231-8017',
    'ambur.r@gmail.com',
    '123456',
    true
  ),
  (
    'Clemmie',
    'Betchley',
    '1973-11-07',
    NULL,
    'clemmie.b@gmail.com',
    'asd123',
    default
  );

--
-- Table structure for table `hotel`
--
DROP TABLE IF EXISTS `hotel`;

CREATE TABLE `hotel` (
  `hotel_id` int NOT NULL AUTO_INCREMENT,
  `hotel_name` varchar(50) NOT NULL,
  `street_address` varchar(50) NOT NULL,
  `city` char(25) NOT NULL,
  `state` char(15) NOT NULL,
  `zipcode` int NOT NULL,
  `phone_number` char(15) NOT NULL,
  `standard_count` int default 0,
  `queen_count` int default 0,
  `king_count` int default 0,
  `standard_price` decimal(10, 2) default 0,
  `queen_price` decimal(10, 2) default 0,
  `king_price` decimal(10, 2) default 0,
  `Pool` boolean default FALSE,
  `Gym` boolean default FALSE,
  `Spa` boolean default FALSE,
  `Bussiness Office` boolean default FALSE,
  `Wifi` boolean default FALSE,
  `weekend_diff_percentage` decimal(3, 2) default 0,
  PRIMARY KEY (`hotel_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Inserting data into hotel table 
INSERT INTO
  `hotel_reservation`.`hotel` (
    `hotel_name`,
    `street_address`,
    `city`,
    `state`,
    `zipcode`,
    `phone_number`,
    `standard_count`,
    `queen_count`,
    `king_count`,
    `Pool`,
    `Gym`,
    `Spa`,
    `Bussiness Office`,
    `Wifi`,
    `standard_price`,
    `queen_price`,
    `king_price`,
    `weekend_diff_percentage`
  )
VALUES
  (
    'The Magnolia All Suites',
    '14187 Commercial Trail',
    'Hampton',
    'VA',
    23452,
    '213-342-5433',
    10,
    5,
    5,
    true,
    true,
    true,
    true,
    false,
    100,
    150,
    250,
    0.25
  ),
  (
    'The Lofts at Town Centre',
    '251 Springs Junction',
    'Colorado Springs',
    'CO',
    54789,
    '532-543-7970',
    20,
    20,
    20,
    true,
    true,
    false,
    true,
    false,
    105,
    120,
    190,
    0.35
  ),
  (
    'Park North Hotel',
    '30 Arapahoe Terrace',
    'Orlando',
    'FL',
    75231,
    '854-324-7653',
    50,
    25,
    25,
    true,
    true,
    false,
    false,
    false,
    50,
    75,
    90,
    0.15
  ),
  (
    'The Courtyard Suites',
    '5 Spohn Circle',
    'Arlington',
    'TX',
    78532,
    '747-231-8017',
    10,
    5,
    5,
    true,
    true,
    true,
    true,
    false,
    100,
    150,
    250,
    0.25
  ),
  (
    'The Regency Rooms',
    '7 Manley Drive',
    'Chicago',
    'IL',
    54932,
    '876-462-1211',
    10,
    5,
    5,
    true,
    true,
    true,
    true,
    false,
    100,
    150,
    250,
    0.25
  ),
  (
    'Town Inn Budget Rooms',
    '50 Lillian Crossing',
    'Nashville',
    'TN',
    68423,
    '210-435-3422',
    75,
    45,
    30,
    true,
    false,
    false,
    false,
    false,
    25,
    50,
    60,
    0.15
  ),
  (
    'The Comfy Motel Place',
    '538 Mosinee Center',
    'Sarasota',
    'FL',
    75765,
    '854-899-4532',
    30,
    20,
    0,
    false,
    false,
    false,
    false,
    false,
    30,
    50,
    0,
    0.1
  ),
  (
    'Sun Palace Inn',
    '3520 Ohio Trail',
    'Visalia',
    'CA',
    97453,
    '634-112-6543',
    30,
    10,
    10,
    true,
    true,
    false,
    false,
    false,
    40,
    60,
    80,
    0.25
  ),
  (
    'HomeAway Inn',
    '68 Lawn Avenue',
    'Atlanta',
    'GA',
    43832,
    '774-332-9943',
    30,
    0,
    0,
    true,
    false,
    false,
    true,
    false,
    50,
    0,
    0,
    0.25
  ),
  (
    'Rio Inn',
    '123 Avenue',
    'Austin',
    'TX',
    78352,
    '210-342-9943',
    20,
    20,
    10,
    true,
    false,
    false,
    false,
    false,
    25,
    55,
    89,
    0.2
  );

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
  `total_price` decimal(10, 2) DEFAULT NULL,
  `reserved_standard_count` int DEFAULT 0,
  `reserved_queen_count` int DEFAULT 0,
  `reserved_king_count` int DEFAULT 0,
  PRIMARY KEY (`reservation_id`),
  CONSTRAINT `reservations_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
