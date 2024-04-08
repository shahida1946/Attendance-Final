-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: studentss
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
-- Table structure for table `attendance_records`
--

DROP TABLE IF EXISTS `attendance_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  `date` date NOT NULL,
  `check_in_time` time DEFAULT NULL,
  `check_out_time` time DEFAULT NULL,
  `status` enum('Present','Absent','Excused') NOT NULL,
  PRIMARY KEY (`record_id`),
  KEY `student_id` (`student_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `attendance_records_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `attendance_records_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_records`
--

LOCK TABLES `attendance_records` WRITE;
/*!40000 ALTER TABLE `attendance_records` DISABLE KEYS */;
INSERT INTO `attendance_records` VALUES (2,14,4,'2024-04-05','18:42:22','20:15:18','Present'),(3,14,4,'2024-01-07',NULL,NULL,'Absent'),(4,14,4,'2024-01-08',NULL,NULL,'Absent'),(5,14,4,'2024-01-09',NULL,NULL,'Absent'),(6,14,4,'2024-01-10',NULL,NULL,'Absent'),(7,14,4,'2024-01-11',NULL,NULL,'Absent'),(8,14,4,'2024-01-12',NULL,NULL,'Absent'),(9,14,4,'2024-01-13',NULL,NULL,'Absent'),(10,14,4,'2024-01-14',NULL,NULL,'Absent'),(11,14,4,'2024-01-15',NULL,NULL,'Absent'),(12,14,4,'2024-01-16',NULL,NULL,'Absent'),(13,14,4,'2024-01-17',NULL,NULL,'Absent'),(14,14,4,'2024-01-18',NULL,NULL,'Absent'),(15,14,4,'2024-01-19',NULL,NULL,'Absent'),(16,14,4,'2024-01-20',NULL,NULL,'Absent'),(17,14,4,'2024-01-21',NULL,NULL,'Absent'),(18,14,4,'2024-01-22',NULL,NULL,'Absent'),(19,14,4,'2024-01-23',NULL,NULL,'Absent'),(20,14,4,'2024-01-24',NULL,NULL,'Absent'),(21,14,4,'2024-01-25',NULL,NULL,'Absent'),(22,14,4,'2024-01-26',NULL,NULL,'Absent'),(23,14,4,'2024-01-27',NULL,NULL,'Absent'),(24,14,4,'2024-01-28',NULL,NULL,'Absent'),(25,14,4,'2024-01-29',NULL,NULL,'Absent'),(26,14,4,'2024-01-30',NULL,NULL,'Absent'),(27,14,4,'2024-01-31',NULL,NULL,'Absent'),(28,14,4,'2024-02-01',NULL,NULL,'Absent'),(29,14,4,'2024-02-02',NULL,NULL,'Absent'),(30,14,4,'2024-02-03',NULL,NULL,'Absent'),(31,14,4,'2024-02-04',NULL,NULL,'Absent'),(32,14,4,'2024-02-05',NULL,NULL,'Absent'),(33,14,4,'2024-02-06',NULL,NULL,'Absent'),(34,14,4,'2024-02-07',NULL,NULL,'Absent'),(35,14,4,'2024-02-08',NULL,NULL,'Absent'),(36,14,4,'2024-02-09',NULL,NULL,'Absent'),(37,14,4,'2024-02-10',NULL,NULL,'Absent'),(38,14,4,'2024-02-11',NULL,NULL,'Absent'),(39,14,4,'2024-02-12',NULL,NULL,'Absent'),(40,14,4,'2024-02-13',NULL,NULL,'Absent'),(41,14,4,'2024-02-14',NULL,NULL,'Absent'),(42,14,4,'2024-02-15',NULL,NULL,'Absent'),(43,14,4,'2024-02-16',NULL,NULL,'Absent'),(44,14,4,'2024-02-17',NULL,NULL,'Absent'),(45,14,4,'2024-02-18',NULL,NULL,'Absent'),(46,14,4,'2024-02-19',NULL,NULL,'Absent'),(47,14,4,'2024-02-20',NULL,NULL,'Absent'),(48,14,4,'2024-02-21',NULL,NULL,'Absent'),(49,14,4,'2024-02-22',NULL,NULL,'Absent'),(50,14,4,'2024-02-23',NULL,NULL,'Absent'),(51,14,4,'2024-02-24',NULL,NULL,'Absent'),(52,14,4,'2024-02-25',NULL,NULL,'Absent'),(53,14,4,'2024-02-26',NULL,NULL,'Absent'),(54,14,4,'2024-02-27',NULL,NULL,'Absent'),(55,14,4,'2024-02-28',NULL,NULL,'Absent'),(56,14,4,'2024-02-29',NULL,NULL,'Absent'),(57,14,4,'2024-03-01',NULL,NULL,'Absent'),(58,14,4,'2024-03-02',NULL,NULL,'Absent'),(59,14,4,'2024-03-03',NULL,NULL,'Absent'),(60,14,4,'2024-03-04',NULL,NULL,'Absent'),(61,14,4,'2024-03-05',NULL,NULL,'Absent'),(62,14,4,'2024-03-06',NULL,NULL,'Absent'),(63,14,4,'2024-03-07',NULL,NULL,'Absent'),(64,14,4,'2024-03-08',NULL,NULL,'Absent'),(65,14,4,'2024-03-09',NULL,NULL,'Absent'),(66,14,4,'2024-03-10',NULL,NULL,'Absent'),(67,14,4,'2024-03-11',NULL,NULL,'Absent'),(68,14,4,'2024-03-12',NULL,NULL,'Absent'),(69,14,4,'2024-03-13',NULL,NULL,'Absent'),(70,14,4,'2024-03-14',NULL,NULL,'Absent'),(71,14,4,'2024-03-15',NULL,NULL,'Absent'),(72,14,4,'2024-03-16',NULL,NULL,'Absent'),(73,14,4,'2024-03-17',NULL,NULL,'Absent'),(74,14,4,'2024-03-18',NULL,NULL,'Absent'),(75,14,4,'2024-03-19',NULL,NULL,'Absent'),(76,14,4,'2024-03-20',NULL,NULL,'Absent'),(77,14,4,'2024-03-21',NULL,NULL,'Absent'),(78,14,4,'2024-03-22',NULL,NULL,'Absent'),(79,14,4,'2024-03-23',NULL,NULL,'Absent'),(80,14,4,'2024-03-24',NULL,NULL,'Absent'),(81,14,4,'2024-03-25',NULL,NULL,'Absent'),(82,14,4,'2024-03-26',NULL,NULL,'Absent'),(83,14,4,'2024-03-27',NULL,NULL,'Absent'),(84,14,4,'2024-03-28',NULL,NULL,'Absent'),(85,14,4,'2024-03-29',NULL,NULL,'Absent'),(86,14,4,'2024-03-30',NULL,NULL,'Absent'),(87,14,4,'2024-03-31',NULL,NULL,'Absent'),(88,14,4,'2024-04-01',NULL,NULL,'Absent'),(89,14,4,'2024-04-02',NULL,NULL,'Absent'),(90,14,4,'2024-04-03',NULL,NULL,'Absent'),(91,14,4,'2024-04-04',NULL,NULL,'Absent'),(92,14,4,'2024-01-06',NULL,NULL,'Absent'),(93,14,4,'2024-04-06','21:59:11','22:01:04','Present');
/*!40000 ALTER TABLE `attendance_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_enrollment`
--

DROP TABLE IF EXISTS `course_enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_enrollment` (
  `enrollment_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`enrollment_id`),
  KEY `student_id` (`student_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `course_enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `course_enrollment_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_enrollment`
--

LOCK TABLES `course_enrollment` WRITE;
/*!40000 ALTER TABLE `course_enrollment` DISABLE KEYS */;
INSERT INTO `course_enrollment` VALUES (1,14,4);
/*!40000 ALTER TABLE `course_enrollment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `department_id` int DEFAULT NULL,
  `course_target` int NOT NULL,
  `target_added_by` int DEFAULT NULL,
  `target_updated_by` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `department_id` (`department_id`),
  KEY `target_added_by` (`target_added_by`),
  KEY `target_updated_by` (`target_updated_by`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `target_added_ibfk_1` FOREIGN KEY (`target_added_by`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `target_updated_ibfk_1` FOREIGN KEY (`target_updated_by`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Introduction to Programming',1,1010,2,2,NULL),(2,'Digital Circuits',2,80,2,3,NULL),(3,'Financial Management',3,120,NULL,NULL,NULL),(4,'Calculus',4,90,1,3,'2024-04-05'),(5,'Mechanics',5,75,NULL,NULL,NULL),(6,'Database Management',1,110,3,1,NULL),(7,'Marketing Strategies',3,100,NULL,NULL,NULL),(8,'Machine Learning',1,130,2,3,NULL),(9,'Microeconomics',3,95,3,1,NULL),(10,'Robotics',5,85,1,2,NULL);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(60) NOT NULL,
  PRIMARY KEY (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Computer Science'),(2,'Electrical Engineering'),(3,'Business Administration'),(4,'Mathematics'),(5,'Mechanical Engineering');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `faculty_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `department_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`faculty_id`),
  KEY `user_id` (`user_id`),
  KEY `department_id` (`department_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `faculty_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `faculty_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `faculty_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (11,2,4,4),(12,3,2,2),(13,6,1,6),(14,7,2,7),(15,9,5,10);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `department_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`student_id`),
  KEY `user_id` (`user_id`),
  KEY `department_id` (`department_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (11,1,1,1),(12,1,2,2),(13,3,3,3),(14,4,4,4),(15,5,5,5),(16,8,3,8),(17,10,5,10);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable` (
  `timetable_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `course_id` int NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `lock_duration` int NOT NULL,
  PRIMARY KEY (`timetable_id`),
  KEY `faculty_id` (`faculty_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `timetable_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `timetable_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
INSERT INTO `timetable` VALUES (2,11,1,'04:00:00','16:00:00',15),(3,11,4,'21:59:00','22:01:00',1);
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `mobileno` varchar(10) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('Admin','Student','Faculty') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'John Doe','johndoe@example.com','Male','1234567890','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Student'),(2,'Jane Smith','janesmith@example.com','Female','9876543210','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Faculty'),(3,'Admin User','admin@example.com','Male','5555555555','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Admin'),(4,'Alice Johnson','alice@example.com','Female','1112223333','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Student'),(5,'Bob Brown','bob@example.com','Male','4445556666','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Student'),(6,'Eva Williams','eva@example.com','Female','7778889999','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Faculty'),(7,'Chris Evans','chris@example.com','Male','9998887777','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Student'),(8,'Olivia Taylor','olivia@example.com','Female','6665554444','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Student'),(9,'David Lee','david@example.com','Male','2223334444','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Faculty'),(10,'Sophia Martinez','sophia@example.com','Female','8889990000','pbkdf2:sha256:600000$mnLlklgYYNL6rQ2m$c405c4a92dfc5e4ba0856de048f52c6f569728f742d7e3fb70c86d158d467184','Student');
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

-- Dump completed on 2024-04-05 22:58:39
