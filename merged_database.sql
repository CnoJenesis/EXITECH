-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_initial` varchar(5) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918','System',NULL,'Administrator',NULL),(4,'1650','d82104464ca5659ce4580eedc33f023bbc8cfd1c96f51598d322cb0fc2b609e0','Algene','T','Radaza',NULL);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:58
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class_schedules`
--

DROP TABLE IF EXISTS `class_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_schedules` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `section_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `teacher_id` int NOT NULL,
  `day_of_week` varchar(10) NOT NULL,
  `time_start` time NOT NULL,
  `time_end` time NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `subject_id` (`subject_id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `idx_schedule_section` (`section_id`),
  KEY `idx_schedule_day_time` (`day_of_week`,`time_start`,`time_end`),
  CONSTRAINT `class_schedules_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`),
  CONSTRAINT `class_schedules_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`),
  CONSTRAINT `class_schedules_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_schedules`
--

LOCK TABLES `class_schedules` WRITE;
/*!40000 ALTER TABLE `class_schedules` DISABLE KEYS */;
INSERT INTO `class_schedules` VALUES (1,19,1,1,'SATURDAY','03:15:00','22:00:00');
/*!40000 ALTER TABLE `class_schedules` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:57
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `exit_logs`
--

DROP TABLE IF EXISTS `exit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exit_logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `status` varchar(20) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `destination` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `idx_exit_logs_student` (`student_id`),
  KEY `idx_exit_logs_timestamp` (`timestamp`),
  CONSTRAINT `exit_logs_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exit_logs`
--

LOCK TABLES `exit_logs` WRITE;
/*!40000 ALTER TABLE `exit_logs` DISABLE KEYS */;
INSERT INTO `exit_logs` VALUES (574,1,'2025-03-21 02:30:32','ALLOWED',NULL,NULL),(575,1,'2025-03-21 02:30:38','ALLOWED',NULL,NULL),(576,1,'2025-03-21 02:30:53','ALLOWED',NULL,NULL),(577,1,'2025-03-21 02:31:13','ALLOWED',NULL,NULL),(578,1,'2025-03-21 02:32:02','ALLOWED',NULL,NULL),(579,3,'2025-03-21 02:32:05','ALLOWED',NULL,NULL),(580,14,'2025-03-21 02:32:11','ALLOWED',NULL,NULL),(581,2,'2025-03-21 02:32:14','ALLOWED',NULL,NULL),(582,2,'2025-03-21 02:33:40','ALLOWED',NULL,NULL),(583,2,'2025-03-21 02:36:44','ALLOWED',NULL,NULL),(584,1,'2025-03-21 02:37:39','ALLOWED',NULL,NULL),(585,1,'2025-03-21 02:37:41','ALLOWED',NULL,NULL),(586,1,'2025-03-21 02:37:42','ALLOWED',NULL,NULL),(587,1,'2025-03-21 02:37:42','ALLOWED',NULL,NULL),(588,2,'2025-03-21 02:37:47','ALLOWED',NULL,NULL),(589,2,'2025-03-21 02:38:03','ALLOWED',NULL,NULL),(590,2,'2025-03-21 02:38:07','ALLOWED',NULL,NULL),(591,2,'2025-03-21 02:44:13','ALLOWED',NULL,NULL),(592,5,'2025-03-21 02:44:20','ALLOWED',NULL,NULL),(593,1,'2025-03-21 02:44:23','ALLOWED',NULL,NULL),(594,1,'2025-03-21 02:44:24','ALLOWED',NULL,NULL),(595,1,'2025-03-21 02:44:27','ALLOWED',NULL,NULL),(596,1,'2025-03-21 02:44:29','ALLOWED',NULL,NULL),(597,5,'2025-03-21 02:44:33','ALLOWED',NULL,NULL),(598,1,'2025-03-21 02:44:38','ALLOWED',NULL,NULL),(599,1,'2025-03-21 02:48:06','ALLOWED',NULL,NULL),(600,1,'2025-03-21 02:48:09','ALLOWED',NULL,NULL),(601,5,'2025-03-21 02:48:28','ALLOWED',NULL,NULL),(602,5,'2025-03-21 02:50:37','ALLOWED',NULL,NULL),(603,1,'2025-03-21 02:50:42','ALLOWED',NULL,NULL),(604,1,'2025-03-21 02:50:54','ALLOWED',NULL,NULL),(605,1,'2025-03-21 02:51:35','ALLOWED',NULL,NULL),(606,24,'2025-03-21 02:51:38','ALLOWED',NULL,NULL),(607,23,'2025-03-21 02:51:39','ALLOWED',NULL,NULL),(608,22,'2025-03-21 02:51:39','ALLOWED',NULL,NULL),(609,20,'2025-03-21 02:51:39','ALLOWED',NULL,NULL),(610,19,'2025-03-21 02:51:40','ALLOWED',NULL,NULL),(611,18,'2025-03-21 02:51:40','ALLOWED',NULL,NULL),(612,17,'2025-03-21 02:51:40','ALLOWED',NULL,NULL),(613,16,'2025-03-21 02:51:40','ALLOWED',NULL,NULL),(614,15,'2025-03-21 02:51:41','ALLOWED',NULL,NULL),(615,15,'2025-03-21 02:51:46','ALLOWED',NULL,NULL),(616,24,'2025-03-21 02:51:49','ALLOWED',NULL,NULL),(617,23,'2025-03-21 02:51:50','ALLOWED',NULL,NULL),(618,20,'2025-03-21 02:51:50','ALLOWED',NULL,NULL),(619,16,'2025-03-21 02:51:51','ALLOWED',NULL,NULL),(620,15,'2025-03-21 02:51:52','ALLOWED',NULL,NULL),(621,17,'2025-03-21 02:51:52','ALLOWED',NULL,NULL),(622,19,'2025-03-21 02:51:52','ALLOWED',NULL,NULL),(623,22,'2025-03-21 02:51:53','ALLOWED',NULL,NULL),(624,24,'2025-03-21 02:51:53','ALLOWED',NULL,NULL),(625,1,'2025-03-21 02:57:19','ALLOWED',NULL,NULL),(626,5,'2025-03-21 02:57:23','ALLOWED',NULL,NULL),(627,1,'2025-03-21 02:57:28','ALLOWED',NULL,NULL),(628,3,'2025-03-21 02:57:35','ALLOWED',NULL,NULL),(629,2,'2025-03-21 02:57:39','ALLOWED',NULL,NULL),(630,3,'2025-03-21 02:57:45','ALLOWED',NULL,NULL),(631,3,'2025-03-21 02:57:50','ALLOWED',NULL,NULL),(632,2,'2025-03-21 02:57:54','ALLOWED',NULL,NULL),(633,3,'2025-03-21 02:57:54','ALLOWED',NULL,NULL),(634,2,'2025-03-21 02:57:55','ALLOWED',NULL,NULL),(635,3,'2025-03-21 02:57:56','ALLOWED',NULL,NULL),(636,5,'2025-03-21 03:00:05','ALLOWED',NULL,NULL),(637,1,'2025-03-21 03:00:06','ALLOWED',NULL,NULL),(638,5,'2025-03-21 03:00:06','ALLOWED',NULL,NULL),(639,1,'2025-03-21 03:00:07','ALLOWED',NULL,NULL),(640,5,'2025-03-21 03:00:08','ALLOWED',NULL,NULL),(641,1,'2025-03-21 03:00:10','ALLOWED',NULL,NULL),(642,1,'2025-03-21 03:00:11','ALLOWED',NULL,NULL),(643,5,'2025-03-21 03:00:14','ALLOWED',NULL,NULL),(644,5,'2025-03-21 03:00:16','ALLOWED',NULL,NULL),(645,5,'2025-03-21 03:00:21','ALLOWED',NULL,NULL),(646,5,'2025-03-21 03:01:20','ALLOWED',NULL,NULL),(647,1,'2025-03-21 03:01:21','ALLOWED',NULL,NULL),(648,5,'2025-03-21 03:01:23','ALLOWED',NULL,NULL),(649,1,'2025-03-21 03:01:24','ALLOWED',NULL,NULL),(650,5,'2025-03-21 03:01:28','ALLOWED',NULL,NULL),(651,1,'2025-03-21 03:01:29','ALLOWED',NULL,NULL),(652,5,'2025-03-21 03:01:31','ALLOWED',NULL,NULL),(653,1,'2025-03-21 03:01:32','ALLOWED',NULL,NULL),(654,1,'2025-03-21 03:09:02','ALLOWED',NULL,NULL),(655,3,'2025-03-21 03:09:13','ALLOWED',NULL,NULL),(656,3,'2025-03-21 03:14:38','ALLOWED',NULL,NULL),(657,4,'2025-03-21 03:14:42','ALLOWED',NULL,NULL),(658,2,'2025-03-21 03:14:46','ALLOWED',NULL,NULL),(659,5,'2025-03-21 03:14:49','ALLOWED',NULL,NULL),(660,1,'2025-03-21 03:14:52','ALLOWED',NULL,NULL),(661,5,'2025-03-21 03:17:46','ALLOWED',NULL,NULL),(662,5,'2025-03-21 03:18:46','ALLOWED',NULL,NULL),(663,2,'2025-03-21 03:24:27','ALLOWED',NULL,NULL),(664,2,'2025-03-21 03:25:46','ALLOWED',NULL,NULL),(665,1,'2025-03-21 03:25:49','ALLOWED',NULL,NULL),(666,5,'2025-03-21 03:25:50','ALLOWED',NULL,NULL),(667,2,'2025-03-21 03:25:51','ALLOWED',NULL,NULL),(668,5,'2025-03-21 03:25:51','ALLOWED',NULL,NULL),(669,3,'2025-03-21 03:26:02','ALLOWED',NULL,NULL),(670,2,'2025-03-21 03:26:10','ALLOWED',NULL,NULL),(671,1,'2025-03-21 03:26:11','ALLOWED',NULL,NULL),(672,1,'2025-03-21 03:26:11','ALLOWED',NULL,NULL),(673,1,'2025-03-21 03:26:14','ALLOWED',NULL,NULL),(674,1,'2025-03-21 03:26:15','ALLOWED',NULL,NULL),(675,1,'2025-03-21 03:26:16','ALLOWED',NULL,NULL),(676,1,'2025-03-21 03:26:17','ALLOWED',NULL,NULL),(677,1,'2025-03-21 03:26:17','ALLOWED',NULL,NULL),(678,1,'2025-03-21 03:31:02','ALLOWED',NULL,NULL),(679,1,'2025-03-21 03:32:01','ALLOWED',NULL,NULL),(680,1,'2025-03-21 03:33:14','ALLOWED',NULL,NULL),(681,1,'2025-03-21 03:33:44','ALLOWED',NULL,NULL),(682,1,'2025-03-21 03:40:53','ALLOWED',NULL,NULL),(683,1,'2025-03-21 03:40:56','ALLOWED',NULL,NULL),(684,1,'2025-03-21 03:41:50','ALLOWED',NULL,NULL),(685,2,'2025-03-21 03:41:55','ALLOWED',NULL,NULL),(686,2,'2025-03-21 03:42:07','ALLOWED',NULL,NULL),(687,2,'2025-03-21 03:42:08','ALLOWED',NULL,NULL),(688,3,'2025-03-21 03:42:11','ALLOWED',NULL,NULL),(689,1,'2025-03-21 03:42:15','ALLOWED',NULL,NULL),(690,1,'2025-03-21 03:42:23','ALLOWED',NULL,NULL),(691,2,'2025-03-21 03:42:27','ALLOWED',NULL,NULL),(692,3,'2025-03-21 03:42:31','ALLOWED',NULL,NULL),(693,3,'2025-03-21 03:42:36','ALLOWED',NULL,NULL),(694,2,'2025-03-21 03:42:40','ALLOWED',NULL,NULL),(695,3,'2025-03-21 03:42:42','ALLOWED',NULL,NULL),(696,1,'2025-03-21 03:42:58','ALLOWED',NULL,NULL),(697,2,'2025-03-21 03:43:13','ALLOWED',NULL,NULL),(698,1,'2025-03-21 03:43:15','ALLOWED',NULL,NULL),(699,2,'2025-03-21 03:44:10','ALLOWED',NULL,NULL),(700,3,'2025-03-21 03:44:12','ALLOWED',NULL,NULL),(701,5,'2025-03-21 03:44:14','ALLOWED',NULL,NULL),(702,4,'2025-03-21 03:44:18','ALLOWED',NULL,NULL),(703,5,'2025-03-21 03:49:25','ALLOWED',NULL,NULL),(704,1,'2025-03-21 03:49:28','ALLOWED',NULL,NULL),(705,3,'2025-03-21 03:49:31','ALLOWED',NULL,NULL),(706,2,'2025-03-21 03:49:35','ALLOWED',NULL,NULL),(707,5,'2025-03-21 03:53:51','ALLOWED',NULL,NULL),(708,2,'2025-03-21 03:53:54','ALLOWED',NULL,NULL),(709,5,'2025-03-21 03:54:00','ALLOWED',NULL,NULL),(710,1,'2025-03-21 03:54:17','ALLOWED',NULL,NULL),(711,3,'2025-03-21 03:54:22','ALLOWED',NULL,NULL),(712,2,'2025-03-21 03:54:26','ALLOWED',NULL,NULL),(713,2,'2025-03-21 04:15:45','ALLOWED',NULL,NULL),(714,1,'2025-03-21 04:15:49','ALLOWED',NULL,NULL),(715,3,'2025-03-21 04:15:55','ALLOWED',NULL,NULL),(716,2,'2025-03-21 04:16:02','ALLOWED',NULL,NULL),(717,3,'2025-03-21 04:16:05','ALLOWED',NULL,NULL),(718,1,'2025-03-21 04:16:37','ALLOWED',NULL,NULL),(719,1,'2025-03-21 04:16:57','ALLOWED',NULL,NULL),(720,2,'2025-03-21 04:17:01','ALLOWED',NULL,NULL),(721,2,'2025-03-21 04:20:41','ALLOWED',NULL,NULL),(722,1,'2025-03-21 04:20:45','ALLOWED',NULL,NULL),(723,5,'2025-03-21 04:24:16','ALLOWED',NULL,NULL),(724,2,'2025-03-21 04:24:20','ALLOWED',NULL,NULL),(725,1,'2025-03-21 04:24:25','ALLOWED',NULL,NULL),(726,4,'2025-03-21 04:24:27','ALLOWED',NULL,NULL),(727,5,'2025-03-21 04:24:34','ALLOWED',NULL,NULL),(728,2,'2025-03-21 04:24:38','ALLOWED',NULL,NULL),(729,1,'2025-03-21 04:24:41','ALLOWED',NULL,NULL),(730,3,'2025-03-21 04:24:44','ALLOWED',NULL,NULL),(731,3,'2025-03-21 04:26:40','ALLOWED',NULL,NULL),(732,4,'2025-03-21 04:26:40','ALLOWED',NULL,NULL),(733,4,'2025-03-21 04:26:41','ALLOWED',NULL,NULL),(734,4,'2025-03-21 04:26:41','ALLOWED',NULL,NULL),(735,3,'2025-03-21 04:26:42','ALLOWED',NULL,NULL),(736,3,'2025-03-21 04:26:42','ALLOWED',NULL,NULL),(737,3,'2025-03-21 04:26:42','ALLOWED',NULL,NULL),(738,3,'2025-03-21 04:26:43','ALLOWED',NULL,NULL),(739,4,'2025-03-21 04:26:43','ALLOWED',NULL,NULL),(740,4,'2025-03-21 04:26:43','ALLOWED',NULL,NULL),(741,4,'2025-03-21 04:26:44','ALLOWED',NULL,NULL),(742,3,'2025-03-21 04:26:44','ALLOWED',NULL,NULL),(743,3,'2025-03-21 04:26:44','ALLOWED',NULL,NULL),(744,3,'2025-03-21 04:27:23','ALLOWED',NULL,NULL),(745,1,'2025-03-21 16:42:43','ALLOWED',NULL,NULL),(746,1,'2025-03-21 16:44:13','ALLOWED',NULL,NULL),(747,1,'2025-03-21 16:48:11','ALLOWED',NULL,NULL),(748,1,'2025-03-21 16:48:35','ALLOWED',NULL,NULL),(749,1,'2025-03-21 16:52:25','ALLOWED',NULL,NULL),(750,1,'2025-03-21 16:54:56','ALLOWED',NULL,NULL),(751,1,'2025-03-21 16:57:37','ALLOWED',NULL,NULL),(752,1,'2025-03-21 16:57:56','ALLOWED',NULL,NULL),(753,1,'2025-03-21 16:58:10','ALLOWED',NULL,NULL),(754,4,'2025-03-21 18:49:42','ALLOWED','Student Exit','Outside Campus'),(755,4,'2025-03-21 18:54:18','ALLOWED','Student Exit','Outside Campus'),(756,1,'2025-03-21 18:54:23','ALLOWED','Student Exit','Outside Campus'),(757,2,'2025-03-21 18:54:25','ALLOWED','Student Exit','Outside Campus'),(758,5,'2025-03-21 18:54:28','ALLOWED','Student Exit','Outside Campus'),(759,3,'2025-03-21 18:54:32','ALLOWED','Student Exit','Outside Campus'),(760,5,'2025-03-21 18:55:55','ALLOWED','Student Exit','Outside Campus'),(761,2,'2025-03-21 18:55:58','ALLOWED','Student Exit','Outside Campus'),(762,5,'2025-03-21 18:57:12','ALLOWED','Student Exit','Outside Campus'),(763,2,'2025-03-21 18:57:14','ALLOWED','Student Exit','Outside Campus'),(764,3,'2025-03-21 18:57:16','ALLOWED','Student Exit','Outside Campus'),(765,1,'2025-03-21 18:57:18','ALLOWED','Student Exit','Outside Campus'),(766,4,'2025-03-21 18:57:20','ALLOWED','Student Exit','Outside Campus'),(767,5,'2025-03-21 18:57:25','ALLOWED','Student Exit','Outside Campus'),(768,5,'2025-03-21 19:09:48','ALLOWED','Student Exit','Outside Campus'),(769,5,'2025-03-21 19:09:55','ALLOWED','Student Exit','Outside Campus'),(770,5,'2025-03-21 19:10:15','ALLOWED','Student Exit','Outside Campus'),(771,2,'2025-03-21 19:10:18','ALLOWED','Student Exit','Outside Campus'),(772,3,'2025-03-21 19:10:20','ALLOWED','Student Exit','Outside Campus'),(773,1,'2025-03-21 19:10:22','ALLOWED','Student Exit','Outside Campus'),(774,4,'2025-03-21 19:10:24','ALLOWED','Student Exit','Outside Campus'),(775,5,'2025-03-21 19:13:56','ALLOWED','Student Exit','Outside Campus'),(776,14,'2025-03-21 19:14:10','ALLOWED','Student Exit','Outside Campus'),(777,13,'2025-03-21 19:14:11','ALLOWED','Student Exit','Outside Campus'),(778,12,'2025-03-21 19:14:12','ALLOWED','Student Exit','Outside Campus'),(779,11,'2025-03-21 19:14:13','ALLOWED','Student Exit','Outside Campus'),(780,10,'2025-03-21 19:14:14','ALLOWED','Student Exit','Outside Campus'),(781,9,'2025-03-21 19:14:15','ALLOWED','Student Exit','Outside Campus'),(782,8,'2025-03-21 19:14:16','ALLOWED','Student Exit','Outside Campus'),(783,7,'2025-03-21 19:14:17','ALLOWED','Student Exit','Outside Campus'),(784,6,'2025-03-21 19:14:18','ALLOWED','Student Exit','Outside Campus'),(785,5,'2025-03-21 19:14:19','ALLOWED','Student Exit','Outside Campus'),(786,25,'2025-03-21 19:14:31','ALLOWED','Student Exit','Outside Campus'),(787,26,'2025-03-21 19:14:33','ALLOWED','Student Exit','Outside Campus'),(788,27,'2025-03-21 19:14:34','ALLOWED','Student Exit','Outside Campus'),(789,28,'2025-03-21 19:14:35','ALLOWED','Student Exit','Outside Campus'),(790,29,'2025-03-21 19:14:35','ALLOWED','Student Exit','Outside Campus'),(791,30,'2025-03-21 19:14:37','ALLOWED','Student Exit','Outside Campus'),(792,34,'2025-03-21 19:14:37','ALLOWED','Student Exit','Outside Campus'),(793,33,'2025-03-21 19:14:39','ALLOWED','Student Exit','Outside Campus'),(794,32,'2025-03-21 19:14:40','ALLOWED','Student Exit','Outside Campus'),(795,31,'2025-03-21 19:14:41','ALLOWED','Student Exit','Outside Campus'),(796,32,'2025-03-21 19:14:41','ALLOWED','Student Exit','Outside Campus'),(797,32,'2025-03-21 19:16:13','ALLOWED','Student Exit','Outside Campus'),(798,32,'2025-03-21 19:19:58','ALLOWED','No class at exit time','Outside Campus'),(799,2,'2025-03-21 19:20:03','ALLOWED','No class at exit time','Outside Campus'),(800,1,'2025-03-21 19:20:06','ALLOWED','No class at exit time','Outside Campus'),(801,3,'2025-03-21 19:20:08','ALLOWED','No class at exit time','Outside Campus'),(802,3,'2025-03-21 19:20:43','ALLOWED','No class at exit time','Outside Campus'),(803,3,'2025-03-21 19:26:44','ALLOWED','No class at exit time','Outside Campus'),(804,3,'2025-03-21 19:26:58','ALLOWED','No class at exit time','Outside Campus'),(805,32,'2025-03-21 19:28:44','ALLOWED','No class at exit time','Outside Campus'),(806,3,'2025-03-21 19:28:46','ALLOWED','No class at exit time','Outside Campus'),(807,2,'2025-03-21 19:28:49','ALLOWED','No class at exit time','Outside Campus'),(808,1,'2025-03-21 19:28:51','ALLOWED','No class at exit time','Outside Campus'),(809,4,'2025-03-21 19:28:53','ALLOWED','No class at exit time','Outside Campus'),(810,3,'2025-03-21 19:28:58','ALLOWED','No class at exit time','Outside Campus'),(811,3,'2025-03-21 19:29:29','DENIED','Classes Ongoing - TEST','Outside Campus'),(812,3,'2025-03-21 19:29:37','DENIED','Classes Ongoing - TEST','Outside Campus'),(813,3,'2025-03-21 19:29:42','DENIED','Classes Ongoing - TEST','Outside Campus'),(814,3,'2025-03-21 19:31:53','DENIED','Classes Ongoing - TEST','Outside Campus'),(815,3,'2025-03-21 19:32:05','DENIED','Classes Ongoing - TEST','Outside Campus'),(816,32,'2025-03-21 19:40:45','ALLOWED','No class at exit time','Outside Campus'),(817,3,'2025-03-21 19:40:47','DENIED','Classes Ongoing - TEST','Outside Campus'),(818,32,'2025-03-21 19:51:37','ALLOWED','No class at exit time','Outside Campus'),(819,3,'2025-03-21 19:51:40','DENIED','Classes Ongoing - TEST','Outside Campus'),(820,2,'2025-03-21 19:51:46','ALLOWED','No class at exit time','Outside Campus'),(821,3,'2025-03-21 19:52:40','DENIED','Student Exit','Outside Campus'),(822,3,'2025-03-21 19:53:08','DENIED','Student Exit','Outside Campus'),(823,3,'2025-03-21 19:54:02','ALLOWED','Student Exit','Outside Campus'),(824,32,'2025-03-21 19:54:07','ALLOWED','Student Exit','Outside Campus'),(825,2,'2025-03-21 19:54:10','ALLOWED','Student Exit','Outside Campus'),(826,1,'2025-03-21 19:54:13','ALLOWED','Student Exit','Outside Campus'),(827,4,'2025-03-21 19:54:15','ALLOWED','Student Exit','Outside Campus'),(828,32,'2025-03-21 19:54:20','ALLOWED','Student Exit','Outside Campus'),(829,3,'2025-03-21 19:54:22','ALLOWED','Student Exit','Outside Campus'),(830,32,'2025-03-21 19:55:59','ALLOWED','No class at exit time','Outside Campus'),(831,3,'2025-03-21 19:56:01','ALLOWED','No class at exit time','Outside Campus'),(832,32,'2025-03-21 19:57:10','ALLOWED','No class at exit time','Outside Campus'),(833,3,'2025-03-21 19:57:11','DENIED','Classes Ongoing - TEST','Outside Campus'),(834,4,'2025-03-21 19:57:16','DENIED','Classes Ongoing - TEST','Outside Campus'),(835,32,'2025-03-21 19:58:22','ALLOWED','No class at exit time','Outside Campus'),(836,4,'2025-03-21 19:58:25','DENIED','Classes Ongoing - TEST','Outside Campus'),(837,4,'2025-03-21 19:58:33','DENIED','Classes Ongoing - TEST','Outside Campus'),(838,4,'2025-03-21 20:03:35','ALLOWED','No class at exit time','Outside Campus'),(839,4,'2025-03-21 20:04:27','ALLOWED','No class at exit time','Outside Campus'),(840,4,'2025-03-21 20:04:45','ALLOWED','No class at exit time','Outside Campus'),(841,4,'2025-03-21 20:05:05','ALLOWED','No class at exit time','Outside Campus'),(842,4,'2025-03-21 20:05:31','ALLOWED','No class at exit time','Outside Campus'),(843,32,'2025-03-21 20:05:35','ALLOWED','No class at exit time','Outside Campus'),(844,3,'2025-03-21 20:05:39','ALLOWED','No class at exit time','Outside Campus'),(845,3,'2025-03-21 20:06:03','ALLOWED','No class at exit time','Outside Campus'),(846,3,'2025-03-21 20:09:53','ALLOWED','No class at exit time','Outside Campus'),(847,3,'2025-03-21 20:13:00','ALLOWED','No class at exit time','Outside Campus'),(848,3,'2025-03-21 20:17:24','ALLOWED','No class at exit time','Outside Campus'),(849,1,'2025-03-21 20:17:29','ALLOWED','No class at exit time','Outside Campus'),(850,3,'2025-03-21 20:17:50','ALLOWED','No class at exit time','Outside Campus'),(851,3,'2025-03-21 20:18:22','DENIED','Classes Ongoing - TEST','Outside Campus'),(852,2,'2025-03-21 20:19:37','ALLOWED','No class at exit time','Outside Campus'),(853,1,'2025-03-21 20:19:39','DENIED','Classes Ongoing - TEST','Outside Campus'),(854,3,'2025-03-21 20:19:49','DENIED','Classes Ongoing - TEST','Outside Campus'),(855,4,'2025-03-21 20:19:51','DENIED','Classes Ongoing - TEST','Outside Campus'),(856,32,'2025-03-21 20:19:55','ALLOWED','No class at exit time','Outside Campus'),(857,1,'2025-03-21 20:49:28','DENIED','Classes Ongoing - TEST','Outside Campus'),(858,2,'2025-03-21 20:49:31','ALLOWED','No class at exit time','Outside Campus'),(859,1,'2025-03-21 22:55:58','ALLOWED','No class at exit time','Outside Campus'),(860,1,'2025-03-21 22:56:21','ALLOWED','No class at exit time','Outside Campus'),(861,3,'2025-03-21 23:05:10','ALLOWED','No class at exit time','Outside Campus'),(862,4,'2025-03-21 23:05:12','ALLOWED','No class at exit time','Outside Campus'),(863,1,'2025-03-21 23:05:15','ALLOWED','No class at exit time','Outside Campus'),(864,2,'2025-03-21 23:06:06','ALLOWED','No class at exit time','Outside Campus'),(865,1,'2025-03-21 23:06:09','ALLOWED','No class at exit time','Outside Campus'),(866,2,'2025-03-21 23:06:11','ALLOWED','No class at exit time','Outside Campus'),(867,4,'2025-03-21 23:06:13','ALLOWED','No class at exit time','Outside Campus'),(868,3,'2025-03-21 23:06:15','ALLOWED','No class at exit time','Outside Campus'),(869,1,'2025-03-21 23:06:17','ALLOWED','No class at exit time','Outside Campus'),(870,1,'2025-03-21 23:08:26','ALLOWED','No class at exit time','Outside Campus'),(871,1,'2025-03-21 23:09:12','ALLOWED','No class at exit time','Outside Campus'),(872,1,'2025-03-22 00:10:52','ALLOWED','No class at exit time','Outside Campus'),(873,3,'2025-03-22 00:10:55','ALLOWED','No class at exit time','Outside Campus'),(874,4,'2025-03-22 00:10:57','ALLOWED','No class at exit time','Outside Campus'),(875,2,'2025-03-22 00:11:00','ALLOWED','No class at exit time','Outside Campus'),(876,1,'2025-03-22 00:11:02','ALLOWED','No class at exit time','Outside Campus'),(877,3,'2025-03-22 00:11:06','ALLOWED','No class at exit time','Outside Campus'),(878,3,'2025-03-22 00:11:11','ALLOWED','No class at exit time','Outside Campus'),(879,3,'2025-03-22 00:27:42','ALLOWED','No class at exit time','Outside Campus'),(880,4,'2025-03-22 00:27:47','ALLOWED','No class at exit time','Outside Campus'),(881,4,'2025-03-22 00:27:50','ALLOWED','No class at exit time','Outside Campus'),(882,4,'2025-03-22 00:27:54','ALLOWED','No class at exit time','Outside Campus'),(883,4,'2025-03-22 00:31:06','ALLOWED','No class at exit time','Outside Campus'),(884,3,'2025-03-22 00:31:08','ALLOWED','No class at exit time','Outside Campus'),(885,3,'2025-03-22 00:31:17','ALLOWED','No class at exit time','Outside Campus'),(886,3,'2025-03-22 00:35:20','ALLOWED','No class at exit time','Outside Campus'),(887,3,'2025-03-22 00:35:27','ALLOWED','No class at exit time','Outside Campus'),(888,3,'2025-03-22 00:36:50','ALLOWED','No class at exit time','Outside Campus'),(889,3,'2025-03-22 00:40:44','ALLOWED','No class at exit time','Outside Campus'),(890,3,'2025-03-22 00:42:12','ALLOWED','No class at exit time','Outside Campus'),(891,4,'2025-03-22 00:42:16','ALLOWED','No class at exit time','Outside Campus'),(892,4,'2025-03-22 00:42:39','ALLOWED','No class at exit time','Outside Campus'),(893,4,'2025-03-22 00:42:51','ALLOWED','No class at exit time','Outside Campus'),(894,4,'2025-03-22 00:43:00','ALLOWED','No class at exit time','Outside Campus'),(895,3,'2025-03-22 00:43:03','ALLOWED','No class at exit time','Outside Campus'),(896,2,'2025-03-22 00:43:05','ALLOWED','No class at exit time','Outside Campus'),(897,4,'2025-03-22 00:45:14','ALLOWED','No class at exit time','Outside Campus'),(898,2,'2025-03-22 00:45:18','ALLOWED','No class at exit time','Outside Campus'),(899,4,'2025-03-22 00:46:08','ALLOWED','No class at exit time','Outside Campus'),(900,2,'2025-03-22 00:46:14','ALLOWED','No class at exit time','Outside Campus'),(901,2,'2025-03-22 00:46:18','ALLOWED','No class at exit time','Outside Campus'),(902,2,'2025-03-22 00:46:19','ALLOWED','No class at exit time','Outside Campus'),(903,2,'2025-03-22 00:46:59','ALLOWED','No class at exit time','Outside Campus'),(904,2,'2025-03-22 00:50:01','ALLOWED','No class at exit time','Outside Campus'),(905,2,'2025-03-22 00:52:24','ALLOWED','No class at exit time','Outside Campus'),(906,4,'2025-03-22 00:52:26','ALLOWED','No class at exit time','Outside Campus'),(907,3,'2025-03-22 00:52:28','ALLOWED','No class at exit time','Outside Campus'),(908,1,'2025-03-22 00:52:30','ALLOWED','No class at exit time','Outside Campus'),(909,1,'2025-03-22 00:53:40','ALLOWED','No class at exit time','Outside Campus'),(910,3,'2025-03-22 00:53:42','ALLOWED','No class at exit time','Outside Campus'),(911,4,'2025-03-22 00:53:44','ALLOWED','No class at exit time','Outside Campus'),(912,4,'2025-03-22 00:56:03','ALLOWED','No class at exit time','Outside Campus'),(913,3,'2025-03-22 00:56:05','ALLOWED','No class at exit time','Outside Campus'),(914,1,'2025-03-22 00:56:08','ALLOWED','No class at exit time','Outside Campus'),(915,2,'2025-03-22 00:56:10','ALLOWED','No class at exit time','Outside Campus'),(916,3,'2025-03-22 00:56:12','ALLOWED','No class at exit time','Outside Campus'),(917,3,'2025-03-22 00:56:17','ALLOWED','No class at exit time','Outside Campus'),(918,2,'2025-03-22 00:57:42','ALLOWED','No class at exit time','Outside Campus'),(919,2,'2025-03-22 00:57:46','ALLOWED','No class at exit time','Outside Campus'),(920,2,'2025-03-22 00:57:47','ALLOWED','No class at exit time','Outside Campus'),(921,2,'2025-03-22 00:57:49','ALLOWED','No class at exit time','Outside Campus'),(922,2,'2025-03-22 00:57:50','ALLOWED','No class at exit time','Outside Campus'),(923,2,'2025-03-22 00:57:52','ALLOWED','No class at exit time','Outside Campus'),(924,2,'2025-03-22 00:58:05','ALLOWED','No class at exit time','Outside Campus'),(925,3,'2025-03-22 00:58:07','ALLOWED','No class at exit time','Outside Campus'),(926,2,'2025-03-22 01:06:11','ALLOWED','No class at exit time','Outside Campus'),(927,2,'2025-03-22 01:06:14','ALLOWED','No class at exit time','Outside Campus'),(928,3,'2025-03-22 01:06:15','ALLOWED','No class at exit time','Outside Campus'),(929,3,'2025-03-22 01:06:19','ALLOWED','No class at exit time','Outside Campus'),(930,3,'2025-03-22 01:06:19','ALLOWED','No class at exit time','Outside Campus'),(931,2,'2025-03-22 01:06:20','ALLOWED','No class at exit time','Outside Campus'),(932,3,'2025-03-22 01:06:21','ALLOWED','No class at exit time','Outside Campus'),(933,2,'2025-03-22 01:06:22','ALLOWED','No class at exit time','Outside Campus'),(934,2,'2025-03-22 01:06:25','ALLOWED','No class at exit time','Outside Campus'),(935,3,'2025-03-22 01:06:27','ALLOWED','No class at exit time','Outside Campus'),(936,2,'2025-03-22 01:06:28','ALLOWED','No class at exit time','Outside Campus'),(937,2,'2025-03-22 01:06:31','ALLOWED','No class at exit time','Outside Campus'),(938,2,'2025-03-22 01:06:31','ALLOWED','No class at exit time','Outside Campus'),(939,2,'2025-03-22 01:06:33','ALLOWED','No class at exit time','Outside Campus'),(940,3,'2025-03-22 01:06:35','ALLOWED','No class at exit time','Outside Campus'),(941,2,'2025-03-22 01:06:36','ALLOWED','No class at exit time','Outside Campus'),(942,2,'2025-03-22 01:06:36','ALLOWED','No class at exit time','Outside Campus'),(943,2,'2025-03-22 01:06:37','ALLOWED','No class at exit time','Outside Campus'),(944,2,'2025-03-22 01:06:37','ALLOWED','No class at exit time','Outside Campus'),(945,2,'2025-03-22 01:06:37','ALLOWED','No class at exit time','Outside Campus'),(946,2,'2025-03-22 01:06:39','ALLOWED','No class at exit time','Outside Campus'),(947,2,'2025-03-22 01:06:39','ALLOWED','No class at exit time','Outside Campus'),(948,3,'2025-03-22 01:06:39','ALLOWED','No class at exit time','Outside Campus'),(949,3,'2025-03-22 01:06:40','ALLOWED','No class at exit time','Outside Campus'),(950,2,'2025-03-22 01:06:40','ALLOWED','No class at exit time','Outside Campus'),(951,3,'2025-03-22 01:06:40','ALLOWED','No class at exit time','Outside Campus'),(952,3,'2025-03-22 01:06:41','ALLOWED','No class at exit time','Outside Campus'),(953,3,'2025-03-22 01:06:41','ALLOWED','No class at exit time','Outside Campus'),(954,2,'2025-03-22 01:06:41','ALLOWED','No class at exit time','Outside Campus'),(955,2,'2025-03-22 01:06:41','ALLOWED','No class at exit time','Outside Campus'),(956,3,'2025-03-22 01:06:42','ALLOWED','No class at exit time','Outside Campus'),(957,3,'2025-03-22 01:06:42','ALLOWED','No class at exit time','Outside Campus'),(958,2,'2025-03-22 01:06:43','ALLOWED','No class at exit time','Outside Campus'),(959,2,'2025-03-22 01:06:43','ALLOWED','No class at exit time','Outside Campus'),(960,2,'2025-03-22 01:06:43','ALLOWED','No class at exit time','Outside Campus'),(961,3,'2025-03-22 01:06:43','ALLOWED','No class at exit time','Outside Campus'),(962,2,'2025-03-22 01:06:44','ALLOWED','No class at exit time','Outside Campus'),(963,2,'2025-03-22 01:06:44','ALLOWED','No class at exit time','Outside Campus'),(964,2,'2025-03-22 01:06:45','ALLOWED','No class at exit time','Outside Campus'),(965,2,'2025-03-22 01:06:45','ALLOWED','No class at exit time','Outside Campus'),(966,2,'2025-03-22 01:06:45','ALLOWED','No class at exit time','Outside Campus'),(967,2,'2025-03-22 01:06:45','ALLOWED','No class at exit time','Outside Campus'),(968,3,'2025-03-22 01:06:46','ALLOWED','No class at exit time','Outside Campus'),(969,2,'2025-03-22 01:06:46','ALLOWED','No class at exit time','Outside Campus'),(970,3,'2025-03-22 01:06:47','ALLOWED','No class at exit time','Outside Campus'),(971,3,'2025-03-22 01:12:28','ALLOWED','No class at exit time','Outside Campus'),(972,3,'2025-03-22 01:19:44','ALLOWED','No class at exit time','Outside Campus'),(973,3,'2025-03-22 01:43:17','ALLOWED','No class at exit time','Outside Campus'),(974,2,'2025-03-22 01:43:19','ALLOWED','No class at exit time','Outside Campus'),(975,1,'2025-03-22 01:43:22','ALLOWED','No class at exit time','Outside Campus'),(976,4,'2025-03-22 01:43:24','ALLOWED','No class at exit time','Outside Campus'),(977,2,'2025-03-22 02:30:15','ALLOWED','No class at exit time','Outside Campus'),(978,2,'2025-03-22 02:30:35','ALLOWED','No class at exit time','Outside Campus'),(979,2,'2025-03-22 02:33:49','ALLOWED','No class at exit time','Outside Campus'),(980,2,'2025-03-22 02:34:45','ALLOWED','No class at exit time','Outside Campus'),(981,2,'2025-03-22 02:37:39','ALLOWED','No class at exit time','Outside Campus'),(982,2,'2025-03-22 02:41:36','ALLOWED','No class at exit time','Outside Campus'),(983,2,'2025-03-22 02:45:22','ALLOWED','No class at exit time','Outside Campus'),(984,3,'2025-03-22 02:45:28','ALLOWED','No class at exit time','Outside Campus'),(985,1,'2025-03-22 02:45:35','ALLOWED','No class at exit time','Outside Campus'),(986,3,'2025-03-22 02:45:51','ALLOWED','No class at exit time','Outside Campus'),(987,3,'2025-03-22 02:46:09','ALLOWED','No class at exit time','Outside Campus'),(988,3,'2025-03-22 02:46:25','ALLOWED','No class at exit time','Outside Campus'),(989,2,'2025-03-22 02:46:32','ALLOWED','No class at exit time','Outside Campus'),(990,4,'2025-03-22 02:48:22','ALLOWED','No class at exit time','Outside Campus'),(991,4,'2025-03-22 02:48:36','ALLOWED','No class at exit time','Outside Campus'),(992,4,'2025-03-22 02:50:17','ALLOWED','No class at exit time','Outside Campus'),(993,2,'2025-03-22 02:54:40','ALLOWED','No class at exit time','Outside Campus'),(994,2,'2025-03-22 02:55:58','ALLOWED','No class at exit time','Outside Campus'),(995,4,'2025-03-22 02:56:03','ALLOWED','No class at exit time','Outside Campus'),(996,2,'2025-03-22 02:58:55','ALLOWED','No class at exit time','Outside Campus'),(997,2,'2025-03-22 03:00:28','ALLOWED','No class at exit time','Outside Campus'),(998,2,'2025-03-22 03:02:15','ALLOWED','No class at exit time','Outside Campus'),(999,2,'2025-03-22 03:02:22','ALLOWED','No class at exit time','Outside Campus'),(1000,2,'2025-03-22 03:03:19','ALLOWED','No class at exit time','Outside Campus'),(1001,2,'2025-03-22 03:04:38','ALLOWED','No class at exit time','Outside Campus'),(1002,4,'2025-03-22 03:04:41','ALLOWED','No class at exit time','Outside Campus'),(1003,4,'2025-03-22 03:09:15','ALLOWED','No class at exit time','Outside Campus'),(1004,4,'2025-03-22 03:14:26','ALLOWED','No class at exit time','Outside Campus'),(1005,4,'2025-03-22 03:18:29','ALLOWED','No class at exit time','Outside Campus'),(1006,2,'2025-03-22 03:18:32','ALLOWED','No class at exit time','Outside Campus'),(1007,1,'2025-03-22 03:18:35','ALLOWED','No class at exit time','Outside Campus'),(1008,3,'2025-03-22 03:18:37','ALLOWED','No class at exit time','Outside Campus'),(1009,3,'2025-03-22 03:20:16','ALLOWED','No class at exit time','Outside Campus'),(1010,1,'2025-03-22 03:20:37','ALLOWED','No class at exit time','Outside Campus'),(1011,1,'2025-03-22 03:20:39','ALLOWED','No class at exit time','Outside Campus'),(1012,1,'2025-03-22 03:22:07','ALLOWED','No class at exit time','Outside Campus'),(1013,1,'2025-03-22 03:23:38','ALLOWED','No class at exit time','Outside Campus'),(1014,2,'2025-03-22 03:23:43','ALLOWED','No class at exit time','Outside Campus'),(1015,4,'2025-03-22 03:23:45','ALLOWED','No class at exit time','Outside Campus'),(1016,3,'2025-03-22 03:23:46','ALLOWED','No class at exit time','Outside Campus'),(1017,3,'2025-03-22 03:23:51','ALLOWED','No class at exit time','Outside Campus'),(1018,3,'2025-03-22 03:24:41','ALLOWED','No class at exit time','Outside Campus'),(1019,3,'2025-03-22 03:25:09','DENIED','Classes Ongoing - TEST','Outside Campus'),(1020,3,'2025-03-22 03:25:14','DENIED','Classes Ongoing - TEST','Outside Campus'),(1021,4,'2025-03-22 03:25:18','DENIED','Classes Ongoing - TEST','Outside Campus'),(1022,3,'2025-03-22 03:25:26','DENIED','Classes Ongoing - TEST','Outside Campus'),(1023,4,'2025-03-22 03:25:30','DENIED','Classes Ongoing - TEST','Outside Campus'),(1024,2,'2025-03-22 03:25:34','ALLOWED','No class at exit time','Outside Campus'),(1025,1,'2025-03-22 03:25:35','DENIED','Classes Ongoing - TEST','Outside Campus'),(1026,1,'2025-03-22 03:25:38','DENIED','Classes Ongoing - TEST','Outside Campus'),(1027,1,'2025-03-22 03:25:44','DENIED','Classes Ongoing - TEST','Outside Campus'),(1028,2,'2025-03-22 03:25:45','ALLOWED','No class at exit time','Outside Campus'),(1029,3,'2025-03-22 03:25:51','DENIED','Classes Ongoing - TEST','Outside Campus'),(1030,3,'2025-03-22 03:25:56','DENIED','Classes Ongoing - TEST','Outside Campus'),(1031,4,'2025-03-22 03:26:02','DENIED','Classes Ongoing - TEST','Outside Campus'),(1032,3,'2025-03-22 03:26:04','DENIED','Classes Ongoing - TEST','Outside Campus'),(1033,3,'2025-03-22 03:27:03','DENIED','Classes Ongoing - TEST','Outside Campus'),(1034,4,'2025-03-22 03:27:06','DENIED','Classes Ongoing - TEST','Outside Campus'),(1035,2,'2025-03-22 03:27:09','ALLOWED','No class at exit time','Outside Campus'),(1036,1,'2025-03-22 03:27:11','DENIED','Classes Ongoing - TEST','Outside Campus'),(1037,3,'2025-03-22 03:30:02','DENIED','Classes Ongoing - TEST','Outside Campus'),(1038,2,'2025-03-22 03:30:04','ALLOWED','No class at exit time','Outside Campus'),(1039,4,'2025-03-22 03:30:07','DENIED','Classes Ongoing - TEST','Outside Campus'),(1040,4,'2025-03-22 03:30:08','DENIED','Classes Ongoing - TEST','Outside Campus'),(1041,4,'2025-03-22 03:30:10','DENIED','Classes Ongoing - TEST','Outside Campus'),(1042,2,'2025-03-22 03:30:12','ALLOWED','No class at exit time','Outside Campus'),(1043,3,'2025-03-22 03:30:14','DENIED','Classes Ongoing - TEST','Outside Campus'),(1044,3,'2025-03-22 03:31:11','DENIED','Classes Ongoing - TEST','Outside Campus'),(1045,4,'2025-03-22 03:31:13','DENIED','Classes Ongoing - TEST','Outside Campus'),(1046,2,'2025-03-22 03:31:15','ALLOWED','No class at exit time','Outside Campus'),(1047,4,'2025-03-22 03:31:17','DENIED','Classes Ongoing - TEST','Outside Campus'),(1048,4,'2025-03-22 03:31:48','DENIED','Classes Ongoing - TEST','Outside Campus'),(1049,3,'2025-03-22 03:33:30','DENIED','Classes Ongoing - TEST','Outside Campus'),(1050,4,'2025-03-22 03:33:41','DENIED','Classes Ongoing - TEST','Outside Campus'),(1051,4,'2025-03-22 03:34:21','DENIED','Classes Ongoing - TEST','Outside Campus'),(1052,3,'2025-03-22 03:34:24','DENIED','Classes Ongoing - TEST','Outside Campus'),(1053,2,'2025-03-22 03:34:26','ALLOWED','No class at exit time','Outside Campus'),(1054,2,'2025-03-22 03:35:47','ALLOWED','No class at exit time','Outside Campus'),(1055,3,'2025-03-22 03:35:54','DENIED','Classes Ongoing - TEST','Outside Campus'),(1056,2,'2025-03-22 03:35:57','ALLOWED','No class at exit time','Outside Campus'),(1057,3,'2025-03-22 03:36:01','DENIED','Classes Ongoing - TEST','Outside Campus'),(1058,2,'2025-03-22 03:36:29','ALLOWED','No class at exit time','Outside Campus'),(1059,2,'2025-03-22 03:37:44','ALLOWED','No class at exit time','Outside Campus'),(1060,4,'2025-03-22 03:38:30','DENIED','Classes Ongoing - TEST','Outside Campus'),(1061,3,'2025-03-22 03:38:31','DENIED','Classes Ongoing - TEST','Outside Campus'),(1062,2,'2025-03-22 03:38:33','ALLOWED','No class at exit time','Outside Campus'),(1063,3,'2025-03-22 03:38:34','DENIED','Classes Ongoing - TEST','Outside Campus'),(1064,4,'2025-03-22 03:38:35','DENIED','Classes Ongoing - TEST','Outside Campus'),(1065,2,'2025-03-22 03:38:36','ALLOWED','No class at exit time','Outside Campus'),(1066,3,'2025-03-22 03:38:37','DENIED','Classes Ongoing - TEST','Outside Campus'),(1067,2,'2025-03-22 03:38:38','ALLOWED','No class at exit time','Outside Campus'),(1068,4,'2025-03-22 03:38:39','DENIED','Classes Ongoing - TEST','Outside Campus'),(1069,3,'2025-03-22 03:38:40','DENIED','Classes Ongoing - TEST','Outside Campus'),(1070,2,'2025-03-22 03:38:41','ALLOWED','No class at exit time','Outside Campus'),(1071,3,'2025-03-22 03:38:42','DENIED','Classes Ongoing - TEST','Outside Campus'),(1072,2,'2025-03-22 03:38:43','ALLOWED','No class at exit time','Outside Campus'),(1073,3,'2025-03-22 03:38:45','DENIED','Classes Ongoing - TEST','Outside Campus'),(1074,2,'2025-03-22 03:38:46','ALLOWED','No class at exit time','Outside Campus'),(1075,2,'2025-03-22 03:55:45','ALLOWED','No class at exit time','Outside Campus'),(1076,1,'2025-03-22 03:56:41','DENIED','Classes Ongoing - TEST','Outside Campus'),(1077,1,'2025-03-22 03:57:15','DENIED','Classes Ongoing - TEST','Outside Campus'),(1078,1,'2025-03-22 04:08:28','DENIED','Classes Ongoing - TEST','Outside Campus'),(1079,1,'2025-03-22 04:22:58','DENIED','Classes Ongoing - TEST','Outside Campus'),(1080,4,'2025-03-22 04:23:02','DENIED','Classes Ongoing - TEST','Outside Campus'),(1081,3,'2025-03-22 04:23:08','DENIED','Classes Ongoing - TEST','Outside Campus'),(1082,3,'2025-03-22 04:24:11','DENIED','Classes Ongoing - TEST','Outside Campus'),(1083,3,'2025-03-22 04:24:30','DENIED','Classes Ongoing - TEST','Outside Campus'),(1084,3,'2025-03-22 04:24:32','DENIED','Classes Ongoing - TEST','Outside Campus'),(1085,4,'2025-03-22 04:24:38','DENIED','Classes Ongoing - TEST','Outside Campus'),(1086,3,'2025-03-22 04:24:41','DENIED','Classes Ongoing - TEST','Outside Campus'),(1087,3,'2025-03-22 04:25:06','DENIED','Classes Ongoing - TEST','Outside Campus'),(1088,1,'2025-03-22 04:25:07','DENIED','Classes Ongoing - TEST','Outside Campus'),(1089,4,'2025-03-22 04:25:08','DENIED','Classes Ongoing - TEST','Outside Campus'),(1090,3,'2025-03-22 04:25:39','DENIED','Classes Ongoing - TEST','Outside Campus'),(1091,1,'2025-03-22 04:25:48','DENIED','Classes Ongoing - TEST','Outside Campus'),(1092,1,'2025-03-22 04:29:20','DENIED','Classes Ongoing - TEST','Outside Campus'),(1093,1,'2025-03-22 04:31:03','DENIED','Classes Ongoing - TEST','Outside Campus'),(1094,1,'2025-03-22 04:36:03','DENIED','Classes Ongoing - TEST','Outside Campus'),(1095,4,'2025-03-22 04:36:06','DENIED','Classes Ongoing - TEST','Outside Campus'),(1096,1,'2025-03-23 02:37:01','ALLOWED','No class at exit time','Outside Campus'),(1097,1,'2025-03-23 02:39:03','ALLOWED','No class at exit time','Outside Campus'),(1098,1,'2025-03-23 02:42:59','ALLOWED','No class at exit time','Outside Campus'),(1099,3,'2025-03-23 02:47:00','ALLOWED','No class at exit time','Outside Campus'),(1100,3,'2025-03-23 02:48:00','ALLOWED','No class at exit time','Outside Campus'),(1101,1,'2025-03-23 02:48:21','ALLOWED','No class at exit time','Outside Campus'),(1102,1,'2025-03-23 02:50:37','ALLOWED','No class at exit time','Outside Campus'),(1103,1,'2025-03-23 02:51:45','ALLOWED','No class at exit time','Outside Campus'),(1104,1,'2025-03-23 02:52:27','ALLOWED','No class at exit time','Outside Campus'),(1105,1,'2025-03-23 02:53:15','ALLOWED','No class at exit time','Outside Campus'),(1106,1,'2025-03-23 02:59:20','ALLOWED','No class at exit time','Outside Campus'),(1107,1,'2025-03-23 03:00:47','ALLOWED','No class at exit time','Outside Campus'),(1108,1,'2025-03-23 03:03:07','ALLOWED','No class at exit time','Outside Campus');
/*!40000 ALTER TABLE `exit_logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:58
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sections` (
  `section_id` int NOT NULL AUTO_INCREMENT,
  `section_name` varchar(50) NOT NULL,
  `grade_level` int NOT NULL,
  `strand_id` int NOT NULL,
  PRIMARY KEY (`section_id`),
  UNIQUE KEY `section_grade_strand` (`section_name`,`grade_level`,`strand_id`),
  KEY `strand_id` (`strand_id`),
  CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`strand_id`) REFERENCES `strands` (`strand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` VALUES (1,'Altruism',11,1),(18,'Altruism',12,1),(2,'Benevolence',11,1),(19,'Benevolence',12,1),(3,'Competence',11,1),(20,'Competence',12,1),(4,'Diligence',11,1),(21,'Diligence',12,1),(5,'Enthusiasm',11,1),(22,'Enthusiasm',12,1),(6,'Friendship',11,1),(23,'Friendship',12,1),(7,'Generosity',11,1),(24,'Generosity',12,1),(8,'Humility',11,1),(25,'Humility',12,1),(9,'Integrity',11,1),(26,'Integrity',12,1),(10,'Justice',11,1),(27,'Justice',12,1),(11,'Kindness',11,1),(28,'Kindness',12,1),(12,'Loyalty',11,1),(29,'Loyalty',12,1),(13,'Modesty',11,1),(30,'Modesty',12,1),(14,'Nobility',11,1),(31,'Nobility',12,1),(15,'Obedience',11,1),(32,'Obedience',12,1),(16,'Peace',11,1),(33,'Peace',12,1),(17,'Quality',11,1),(34,'Quality',12,1),(35,'Respect',12,1),(36,'Responsibility',11,2),(39,'Responsibility',12,2),(37,'Sincerity',11,2),(40,'Sincerity',12,2),(38,'Tenacity',11,2),(41,'Tenacity',12,2),(42,'Wisdom',11,3),(43,'Wisdom',12,3);
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:58
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `strands`
--

DROP TABLE IF EXISTS `strands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strands` (
  `strand_id` int NOT NULL AUTO_INCREMENT,
  `strand_name` varchar(50) NOT NULL,
  `strand_code` varchar(10) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`strand_id`),
  UNIQUE KEY `strand_name` (`strand_name`),
  UNIQUE KEY `strand_code` (`strand_code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strands`
--

LOCK TABLES `strands` WRITE;
/*!40000 ALTER TABLE `strands` DISABLE KEYS */;
INSERT INTO `strands` VALUES (1,'Science, Technology, Engineering, and Mathematics','STEM','STEM Strand'),(2,'Accountancy, Business, and Management','ABM','ABM Strand'),(3,'General Academic Strand','GAS','GAS Strand');
/*!40000 ALTER TABLE `strands` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:58
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `id_number` varchar(20) NOT NULL,
  `rfid_uid` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_initial` varchar(5) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `grade_level` int NOT NULL,
  `strand_id` int NOT NULL,
  `section_id` int NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `id_number` (`id_number`),
  UNIQUE KEY `rfid_uid` (`rfid_uid`),
  KEY `section_id` (`section_id`),
  KEY `strand_id` (`strand_id`),
  KEY `idx_student_rfid` (`rfid_uid`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`),
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`strand_id`) REFERENCES `strands` (`strand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'23-1206-294','1238852786','ELJHON STEVE','L','SATSAT',NULL,12,1,19,'SATSAT.png'),(2,'23-4474-290','1238529746','ROSSJERSLEY JOHN','G','VILLARICO',NULL,12,1,26,'VILLARICO.jpg'),(3,'23-1195-802','0949993986','SOPHIA MARGAUX ELIZABETH WINNIEFRED SIMONE MAXINE','R','CHU',NULL,12,1,19,'CHU.jpg'),(4,'23-1193-374','1239051858','RIGIE MARK','G','PATAYTAY',NULL,12,1,19,'PATAYTAY.JPG'),(5,'23-5474-290','0950435186','CHIPPY','D','MCDONALD',NULL,12,1,18,''),(6,'23-5206-294','0950932562','KOKOY','H','VILLAMIN',NULL,12,1,19,NULL),(7,'24-5475-291','0950453186','MARCUS','D','SANTOS',NULL,11,1,3,NULL),(8,'24-5207-295','1239109954','ANDREA','N','REYES',NULL,11,1,4,NULL),(9,'24-5476-292','0950479138','JOSHUA','M','TAN',NULL,11,1,5,NULL),(10,'23-5208-296','1238365394','SOFIA','M','GARCIA',NULL,12,1,20,NULL),(11,'24-5477-293','0944373858','RAFAEL','A','CRUZ',NULL,11,1,6,NULL),(12,'24-5209-297','0949881154','ISABELLA','C','LIM',NULL,11,1,7,NULL),(13,'23-5478-294','0950041970','NATHAN','J','YU',NULL,12,1,21,NULL),(14,'24-5210-298','0949724770','SAMANTHA','R','DELA CRUZ',NULL,11,1,8,NULL),(15,'24-5479-295','0949909138','GABRIEL','L','SANTOS',NULL,11,1,9,NULL),(16,'23-5211-299','0953028530','EMMA','P','MENDOZA',NULL,12,1,22,NULL),(17,'24-5480-296','0949918514','LUCAS','M','RAMOS',NULL,11,2,36,NULL),(18,'24-5212-300','0950464482','SOPHIA','G','AQUINO',NULL,11,2,37,NULL),(19,'23-5481-297','0949953650','DAVID','A','TORRES',NULL,12,2,39,NULL),(20,'24-5213-301','0943563106','MIA','C','VILLANUEVA',NULL,11,2,38,NULL),(21,'23-5482-298','0949862706','BENJAMIN','J','LAO',NULL,12,2,40,NULL),(22,'23-5214-302','0950452290','VICTORIA','A','PASCUAL',NULL,12,2,41,NULL),(23,'24-5483-299','0949853314','CHRISTIAN','P','LOPEZ',NULL,11,3,42,NULL),(24,'24-5215-303','0949769202','OLIVIA','F','SANTOS',NULL,11,3,42,NULL),(25,'23-5484-300','0949872866','MATTHEW','J','REYES',NULL,12,3,43,NULL),(26,'24-5216-304','0949863794','CHLOE','M','GARCIA',NULL,11,3,42,NULL),(27,'23-5485-301','0950008834','DANIEL','P','TAN',NULL,12,3,43,NULL),(28,'24-5217-305','0949759794','SOPHIA','E','LIM',NULL,11,1,10,NULL),(29,'23-5486-302','0950505058','ADRIAN','G','YU',NULL,12,1,23,NULL),(30,'24-5218-306','0950669458','HANNAH','M','DELA CRUZ',NULL,11,1,11,NULL),(31,'23-5001-529','0950547922','MILKY','S','SECUYA',NULL,12,1,24,NULL),(32,'23-1000-102','0949806946','MARY GRACE','A','PIATTOS',NULL,12,1,25,NULL),(33,'23-1500-152','0950085426','FERNANDO','B','TEMPURA',NULL,12,1,26,NULL),(34,'23-2000-202','1238518242','CARLOS MIGUEL','C','OISHI',NULL,12,1,27,NULL);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:57
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `subject_code` varchar(20) NOT NULL,
  `subject_name` varchar(100) NOT NULL,
  PRIMARY KEY (`subject_id`),
  UNIQUE KEY `subject_code` (`subject_code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES (1,'TEST','TEST');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:58
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: exitech
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `teacher_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `middle_initial` varchar(5) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'TEST','TEST','TEST','test@test.test');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23  3:20:58
