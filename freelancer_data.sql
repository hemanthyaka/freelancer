-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: freelancer_marketplace
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `certifications`
--

DROP TABLE IF EXISTS `certifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certifications` (
  `certification_id` int NOT NULL AUTO_INCREMENT,
  `freelancer_id` int DEFAULT NULL,
  `certification_name` varchar(255) DEFAULT NULL,
  `certificate_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`certification_id`),
  KEY `freelancer_id` (`freelancer_id`),
  CONSTRAINT `certifications_ibfk_1` FOREIGN KEY (`freelancer_id`) REFERENCES `freelancer` (`freelancer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certifications`
--

LOCK TABLES `certifications` WRITE;
/*!40000 ALTER TABLE `certifications` DISABLE KEYS */;
INSERT INTO `certifications` VALUES (5,32,'FRONTEND DEVELOPER ','S8aG9m');
/*!40000 ALTER TABLE `certifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `gst_number` varchar(15) NOT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `linkedin_profile` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`gst_number`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`),
  UNIQUE KEY `linkedin_profile` (`linkedin_profile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES ('GST123456789','WebDeveloperS','yakahemanth3@gmail.com','8341434767','Andhra Pradesh, India','IT','https://linkedin.com','123');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_projects`
--

DROP TABLE IF EXISTS `company_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_projects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `gst_number` varchar(15) DEFAULT NULL,
  `project_name` varchar(100) DEFAULT NULL,
  `description` text,
  `bid_amount` decimal(10,2) DEFAULT NULL,
  `skills` varchar(255) DEFAULT NULL,
  `requirements` text,
  `job_location` varchar(100) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  KEY `fk_gst_number` (`gst_number`),
  CONSTRAINT `fk_gst_number` FOREIGN KEY (`gst_number`) REFERENCES `companies` (`gst_number`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_projects`
--

LOCK TABLES `company_projects` WRITE;
/*!40000 ALTER TABLE `company_projects` DISABLE KEYS */;
INSERT INTO `company_projects` VALUES (25,'GST123456789','Freelancing Market Place','A freelancing website is a platform where you can earn money for yourself by offering your services as a freelancer. Unlike working for a specific company, freelancers take on specific projects for clients without committing to full-time employment. Here are some key points to consider when describing a freelancing website:',15000.00,'HTML5,CSS3,BOOTSTRAP,JAVASCRIPT,PYTHON,FLASK,MYSQL','Freelancing involves doing specific work for clients without being tied to a full-time job.\r\nFreelancers often manage multiple projects simultaneously.\r\nThe Internal Revenue Service (IRS) considers freelancers to be self-employed individuals.','Coimbatore','2024-05-25','2024-07-01');
/*!40000 ALTER TABLE `company_projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contactus`
--

DROP TABLE IF EXISTS `contactus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactus` (
  `contact_id` int NOT NULL AUTO_INCREMENT,
  `gst_number` varchar(15) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `message` text,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `projectid` int DEFAULT NULL,
  PRIMARY KEY (`contact_id`),
  KEY `gst_number` (`gst_number`),
  CONSTRAINT `contactus_ibfk_1` FOREIGN KEY (`gst_number`) REFERENCES `companies` (`gst_number`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactus`
--

LOCK TABLES `contactus` WRITE;
/*!40000 ALTER TABLE `contactus` DISABLE KEYS */;
INSERT INTO `contactus` VALUES (16,'GST123456789','SD.IMRAN','i can do this project for 20K','9121imran@gmail.com','9121461636',25);
/*!40000 ALTER TABLE `contactus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `freelancer`
--

DROP TABLE IF EXISTS `freelancer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `freelancer` (
  `freelancer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `account_creation_date` date DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `availability` tinyint(1) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `experience` int DEFAULT NULL,
  `institution_name` varchar(255) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT '0.00',
  `working_hours` int DEFAULT '0',
  PRIMARY KEY (`freelancer_id`),
  UNIQUE KEY `name` (`name`),
  KEY `username` (`username`),
  CONSTRAINT `freelancer_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `freelancer`
--

LOCK TABLES `freelancer` WRITE;
/*!40000 ALTER TABLE `freelancer` DISABLE KEYS */;
INSERT INTO `freelancer` VALUES (32,'Hemanth Yaka','yakahemanth3@gmail.com','2024-05-12','W0vY0n',1,'Chennai',1,'PBS ',2024,'hemanthyaka',50000.00,6);
/*!40000 ALTER TABLE `freelancer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `freelancer_id` int DEFAULT NULL,
  `project_name` varchar(255) DEFAULT NULL,
  `description` text,
  `project_image` varchar(255) DEFAULT NULL,
  `completion_date` date DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  KEY `freelancer_id` (`freelancer_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`freelancer_id`) REFERENCES `freelancer` (`freelancer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (18,32,'Foodie','Food is any substance consumed by an organism for nutritional support. Food is usually of plant, animal, or fungal origin and contains essential nutrients such as carbohydrates, fats, proteins, vitamins, or minerals. The substance is ingested by an organism and assimilated by the organism\'s cells to provide energy, maintain life, or stimulate growth. Different species of animals have different feeding behaviours that satisfy the needs of their metabolisms and have evolved to fill a specific ecological niche within specific geographical contexts.','G6uO6v','2024-03-01');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `freelancer_id` int DEFAULT NULL,
  `reviewer_name` varchar(255) DEFAULT NULL,
  `review_text` text,
  `rating` decimal(3,2) DEFAULT NULL,
  `review_date` date DEFAULT NULL,
  `review_time` time DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `freelancer_id` (`freelancer_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`freelancer_id`) REFERENCES `freelancer` (`freelancer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `skill_id` int NOT NULL AUTO_INCREMENT,
  `freelancer_id` int DEFAULT NULL,
  `skill_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`skill_id`),
  KEY `freelancer_id` (`freelancer_id`),
  CONSTRAINT `skills_ibfk_1` FOREIGN KEY (`freelancer_id`) REFERENCES `freelancer` (`freelancer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (11,32,'HTML,CSS,JS,BOOTSTRAP');
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(50) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('hemanthyaka','Yaka','Hemanth','yakahemanth3@gmail.com','+91 8341434767','123');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-14 16:38:29
