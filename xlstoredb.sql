-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 06, 2018 at 01:15 PM
-- Server version: 10.1.25-MariaDB
-- PHP Version: 7.1.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `xlstoredb`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add permission', 3, 'add_permission'),
(8, 'Can change permission', 3, 'change_permission'),
(9, 'Can delete permission', 3, 'delete_permission'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add user', 7, 'add_user'),
(20, 'Can change user', 7, 'change_user'),
(21, 'Can delete user', 7, 'delete_user'),
(22, 'Can add post mention', 8, 'add_postmention'),
(23, 'Can change post mention', 8, 'change_postmention'),
(24, 'Can delete post mention', 8, 'delete_postmention'),
(25, 'Can add post replies', 9, 'add_postreplies'),
(26, 'Can change post replies', 9, 'change_postreplies'),
(27, 'Can delete post replies', 9, 'delete_postreplies'),
(28, 'Can add product comments', 10, 'add_productcomments'),
(29, 'Can change product comments', 10, 'change_productcomments'),
(30, 'Can delete product comments', 10, 'delete_productcomments'),
(31, 'Can add products', 11, 'add_products'),
(32, 'Can change products', 11, 'change_products'),
(33, 'Can delete products', 11, 'delete_products'),
(34, 'Can add product trade', 12, 'add_producttrade'),
(35, 'Can change product trade', 12, 'change_producttrade'),
(36, 'Can delete product trade', 12, 'delete_producttrade'),
(37, 'Can add advertisments', 13, 'add_advertisments'),
(38, 'Can change advertisments', 13, 'change_advertisments'),
(39, 'Can delete advertisments', 13, 'delete_advertisments'),
(40, 'Can add company', 14, 'add_company'),
(41, 'Can change company', 14, 'change_company'),
(42, 'Can delete company', 14, 'delete_company'),
(43, 'Can add user notifications', 15, 'add_usernotifications'),
(44, 'Can change user notifications', 15, 'change_usernotifications'),
(45, 'Can delete user notifications', 15, 'delete_usernotifications'),
(46, 'Can add product interess', 16, 'add_productinteress'),
(47, 'Can change product interess', 16, 'change_productinteress'),
(48, 'Can delete product interess', 16, 'delete_productinteress'),
(49, 'Can add product trade messages', 17, 'add_producttrademessages'),
(50, 'Can change product trade messages', 17, 'change_producttrademessages'),
(51, 'Can delete product trade messages', 17, 'delete_producttrademessages'),
(52, 'Can add posts', 18, 'add_posts'),
(53, 'Can change posts', 18, 'change_posts'),
(54, 'Can delete posts', 18, 'delete_posts'),
(55, 'Can add followers', 19, 'add_followers'),
(56, 'Can change followers', 19, 'change_followers'),
(57, 'Can delete followers', 19, 'delete_followers'),
(58, 'Can add categories', 20, 'add_categories'),
(59, 'Can change categories', 20, 'change_categories'),
(60, 'Can delete categories', 20, 'delete_categories'),
(61, 'Can add product mention', 21, 'add_productmention'),
(62, 'Can change product mention', 21, 'change_productmention'),
(63, 'Can delete product mention', 21, 'delete_productmention'),
(64, 'Can add user follow', 22, 'add_userfollow'),
(65, 'Can change user follow', 22, 'change_userfollow'),
(66, 'Can delete user follow', 22, 'delete_userfollow'),
(67, 'Can add product pictures', 23, 'add_productpictures'),
(68, 'Can change product pictures', 23, 'change_productpictures'),
(69, 'Can delete product pictures', 23, 'delete_productpictures'),
(70, 'Can add m s_ products', 24, 'add_ms_products'),
(71, 'Can change m s_ products', 24, 'change_ms_products'),
(72, 'Can delete m s_ products', 24, 'delete_ms_products'),
(73, 'Can add company notifications', 25, 'add_companynotifications'),
(74, 'Can change company notifications', 25, 'change_companynotifications'),
(75, 'Can delete company notifications', 25, 'delete_companynotifications'),
(76, 'Can add m s_ receipt details', 26, 'add_ms_receiptdetails'),
(77, 'Can change m s_ receipt details', 26, 'change_ms_receiptdetails'),
(78, 'Can delete m s_ receipt details', 26, 'delete_ms_receiptdetails'),
(79, 'Can add m s_ receipts', 27, 'add_ms_receipts'),
(80, 'Can change m s_ receipts', 27, 'change_ms_receipts'),
(81, 'Can delete m s_ receipts', 27, 'delete_ms_receipts'),
(82, 'Can add m s_ product entry', 28, 'add_ms_productentry'),
(83, 'Can change m s_ product entry', 28, 'change_ms_productentry'),
(84, 'Can delete m s_ product entry', 28, 'delete_ms_productentry'),
(85, 'Can add m s_ licence key', 29, 'add_ms_licencekey'),
(86, 'Can change m s_ licence key', 29, 'change_ms_licencekey'),
(87, 'Can delete m s_ licence key', 29, 'delete_ms_licencekey'),
(88, 'Can add m s_ company administrator', 30, 'add_ms_companyadministrator'),
(89, 'Can change m s_ company administrator', 30, 'change_ms_companyadministrator'),
(90, 'Can delete m s_ company administrator', 30, 'delete_ms_companyadministrator'),
(91, 'Can add trade agreement', 31, 'add_tradeagreement'),
(92, 'Can change trade agreement', 31, 'change_tradeagreement'),
(93, 'Can delete trade agreement', 31, 'delete_tradeagreement'),
(94, 'Can add trade agreements', 32, 'add_tradeagreements'),
(95, 'Can change trade agreements', 32, 'change_tradeagreements'),
(96, 'Can delete trade agreements', 32, 'delete_tradeagreements'),
(97, 'Can add m s_ settings', 33, 'add_ms_settings'),
(98, 'Can change m s_ settings', 33, 'change_ms_settings'),
(99, 'Can delete m s_ settings', 33, 'delete_ms_settings'),
(100, 'Can add m s_ market access', 34, 'add_ms_marketaccess'),
(101, 'Can change m s_ market access', 34, 'change_ms_marketaccess'),
(102, 'Can delete m s_ market access', 34, 'delete_ms_marketaccess'),
(103, 'Can add m s_ licence key activations', 35, 'add_ms_licencekeyactivations'),
(104, 'Can change m s_ licence key activations', 35, 'change_ms_licencekeyactivations'),
(105, 'Can delete m s_ licence key activations', 35, 'delete_ms_licencekeyactivations'),
(106, 'Can add company categories', 36, 'add_companycategories'),
(107, 'Can change company categories', 36, 'change_companycategories'),
(108, 'Can delete company categories', 36, 'delete_companycategories'),
(109, 'Can add user categories', 37, 'add_usercategories'),
(110, 'Can change user categories', 37, 'change_usercategories'),
(111, 'Can delete user categories', 37, 'delete_usercategories'),
(112, 'Can add m s_ company teller', 38, 'add_ms_companyteller'),
(113, 'Can change m s_ company teller', 38, 'change_ms_companyteller'),
(114, 'Can delete m s_ company teller', 38, 'delete_ms_companyteller'),
(115, 'Can add address', 39, 'add_address'),
(116, 'Can change address', 39, 'change_address'),
(117, 'Can delete address', 39, 'delete_address'),
(118, 'Can add m s_ market sales details', 40, 'add_ms_marketsalesdetails'),
(119, 'Can change m s_ market sales details', 40, 'change_ms_marketsalesdetails'),
(120, 'Can delete m s_ market sales details', 40, 'delete_ms_marketsalesdetails'),
(121, 'Can add m s_ market sales', 41, 'add_ms_marketsales'),
(122, 'Can change m s_ market sales', 41, 'change_ms_marketsales'),
(123, 'Can delete m s_ market sales', 41, 'delete_ms_marketsales'),
(124, 'Can add m s_ market access', 42, 'add_ms_marketaccess'),
(125, 'Can change m s_ market access', 42, 'change_ms_marketaccess'),
(126, 'Can delete m s_ market access', 42, 'delete_ms_marketaccess'),
(127, 'Can add m s_ market sales', 43, 'add_ms_marketsales'),
(128, 'Can change m s_ market sales', 43, 'change_ms_marketsales'),
(129, 'Can delete m s_ market sales', 43, 'delete_ms_marketsales'),
(130, 'Can add m s_ market sales details', 44, 'add_ms_marketsalesdetails'),
(131, 'Can change m s_ market sales details', 44, 'change_ms_marketsalesdetails'),
(132, 'Can delete m s_ market sales details', 44, 'delete_ms_marketsalesdetails'),
(133, 'Can add e c_ market sales', 43, 'add_ec_marketsales'),
(134, 'Can change e c_ market sales', 43, 'change_ec_marketsales'),
(135, 'Can delete e c_ market sales', 43, 'delete_ec_marketsales'),
(136, 'Can add e c_ market sales details', 44, 'add_ec_marketsalesdetails'),
(137, 'Can change e c_ market sales details', 44, 'change_ec_marketsalesdetails'),
(138, 'Can delete e c_ market sales details', 44, 'delete_ec_marketsalesdetails'),
(139, 'Can add e c_ market access', 42, 'add_ec_marketaccess'),
(140, 'Can change e c_ market access', 42, 'change_ec_marketaccess'),
(141, 'Can delete e c_ market access', 42, 'delete_ec_marketaccess'),
(142, 'Can add e c_ shopping cart items', 44, 'add_ec_shoppingcartitems'),
(143, 'Can change e c_ shopping cart items', 44, 'change_ec_shoppingcartitems'),
(144, 'Can delete e c_ shopping cart items', 44, 'delete_ec_shoppingcartitems'),
(145, 'Can add e c_ shopping cart', 43, 'add_ec_shoppingcart'),
(146, 'Can change e c_ shopping cart', 43, 'change_ec_shoppingcart'),
(147, 'Can delete e c_ shopping cart', 43, 'delete_ec_shoppingcart'),
(148, 'Can add e c_ company settings', 45, 'add_ec_companysettings'),
(149, 'Can change e c_ company settings', 45, 'change_ec_companysettings'),
(150, 'Can delete e c_ company settings', 45, 'delete_ec_companysettings'),
(151, 'Can add e c_ company mobile', 46, 'add_ec_companymobile'),
(152, 'Can change e c_ company mobile', 46, 'change_ec_companymobile'),
(153, 'Can delete e c_ company mobile', 46, 'delete_ec_companymobile'),
(154, 'Can add m s_ company mobile', 47, 'add_ms_companymobile'),
(155, 'Can change m s_ company mobile', 47, 'change_ms_companymobile'),
(156, 'Can delete m s_ company mobile', 47, 'delete_ms_companymobile');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$36000$ytpnbsqttXSC$MYELjr3Vhmz6j2XRo7T37/SJCed0PpCvpdR1k7EbP08=', '2017-10-28 02:49:25.770000', 1, 'chriscott', '', '', 'irchristianscott@gmail.com', 1, 1, '2017-10-11 17:00:25.202000'),
(2, 'pbkdf2_sha256$36000$QEcvcgzMFKsJ$43YKagcHa09Q5oIHwPOqZJDfa6g5ZTrBTRdsKnYQuwc=', '2018-01-16 14:16:31.884067', 1, 'chriscons', '', '', 'irchristianscott@gmail.com', 1, 1, '2018-01-16 14:16:19.136357'),
(3, 'pbkdf2_sha256$36000$AUwIBAZYhRSU$c2sV+UVZJ0/hvVpjvwW218iI1ezDi74nGRpkyWl4mJM=', '2018-03-01 17:30:50.102864', 1, 'admin', '', '', 'irchristianscott@gmail.com', 1, 1, '2018-03-01 17:30:12.088732');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2017-10-28 04:39:51.871000', '1', 'ChriscotTech Inc', 2, '[{\"changed\": {\"fields\": [\"company\", \"status\", \"ammount\", \"expary_date\"]}}]', 29, 1),
(2, '2017-10-28 04:42:14.568000', '2', 'Hosana Textile', 2, '[{\"changed\": {\"fields\": [\"company\", \"status\", \"ammount\", \"expary_date\"]}}]', 29, 1),
(3, '2017-10-28 04:45:19.929000', '1', 'ChriscotTech Inc', 2, '[{\"changed\": {\"fields\": [\"company\", \"ammount\"]}}]', 29, 1),
(4, '2017-11-09 04:29:09.043000', '1', 'Fashion', 1, '[{\"added\": {}}]', 36, 1),
(5, '2017-11-09 04:30:09.228000', '2', 'Beauty', 1, '[{\"added\": {}}]', 36, 1),
(6, '2017-11-09 04:30:48.604000', '3', 'Electronic', 1, '[{\"added\": {}}]', 36, 1),
(7, '2017-11-09 04:31:18.221000', '4', 'Fourniture', 1, '[{\"added\": {}}]', 36, 1),
(8, '2017-11-09 04:31:58.222000', '5', 'Stationary', 1, '[{\"added\": {}}]', 36, 1),
(9, '2017-11-09 04:36:13.218000', '6', 'Mechanical', 1, '[{\"added\": {}}]', 36, 1),
(10, '2017-11-09 04:37:22.603000', '7', 'House & Appartement', 1, '[{\"added\": {}}]', 36, 1),
(11, '2017-11-09 04:37:59.095000', '8', 'Hardware', 1, '[{\"added\": {}}]', 36, 1),
(12, '2017-11-09 04:38:30.371000', '9', 'Music', 1, '[{\"added\": {}}]', 36, 1),
(13, '2017-11-09 04:39:14.973000', '10', 'Others', 1, '[{\"added\": {}}]', 36, 1),
(14, '2018-01-20 16:48:49.440527', '10', 'Others', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(15, '2018-01-20 16:49:10.295656', '9', 'Music', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(16, '2018-01-20 16:49:18.670592', '8', 'Hardware', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(17, '2018-01-20 16:49:27.235094', '7', 'House & Appartement', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(18, '2018-01-20 16:49:36.773265', '6', 'Mechanical', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(19, '2018-01-20 16:49:46.036135', '5', 'Stationary', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(20, '2018-01-20 16:50:00.908931', '4', 'Furniture', 2, '[{\"changed\": {\"fields\": [\"name\", \"image\"]}}]', 36, 2),
(21, '2018-01-20 16:50:14.730343', '3', 'Electronic', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(22, '2018-01-20 16:50:28.395751', '2', 'Beauty', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(23, '2018-01-20 16:50:42.130267', '1', 'Fashion', 2, '[{\"changed\": {\"fields\": [\"image\"]}}]', 36, 2),
(24, '2018-01-20 16:51:37.336363', '11', 'Discotec', 1, '[{\"added\": {}}]', 36, 2),
(25, '2018-01-20 16:52:38.023118', '12', 'Grocery', 1, '[{\"added\": {}}]', 36, 2),
(26, '2018-01-20 16:53:29.492762', '13', 'Library', 1, '[{\"added\": {}}]', 36, 2),
(27, '2018-01-20 16:54:49.325618', '14', 'Medicinal', 1, '[{\"added\": {}}]', 36, 2),
(28, '2018-01-20 16:55:29.830321', '15', 'Restaurants and Bars', 1, '[{\"added\": {}}]', 36, 2),
(29, '2018-01-21 13:23:08.172592', '15', 'Restaurants & Bars', 2, '[{\"changed\": {\"fields\": [\"name\"]}}]', 36, 2);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(39, 'xlstore', 'address'),
(13, 'xlstore', 'advertisments'),
(20, 'xlstore', 'categories'),
(14, 'xlstore', 'company'),
(36, 'xlstore', 'companycategories'),
(25, 'xlstore', 'companynotifications'),
(19, 'xlstore', 'followers'),
(24, 'xlstore', 'ms_products'),
(8, 'xlstore', 'postmention'),
(9, 'xlstore', 'postreplies'),
(18, 'xlstore', 'posts'),
(10, 'xlstore', 'productcomments'),
(16, 'xlstore', 'productinteress'),
(21, 'xlstore', 'productmention'),
(23, 'xlstore', 'productpictures'),
(11, 'xlstore', 'products'),
(12, 'xlstore', 'producttrade'),
(17, 'xlstore', 'producttrademessages'),
(31, 'xlstore', 'tradeagreement'),
(32, 'xlstore', 'tradeagreements'),
(7, 'xlstore', 'user'),
(37, 'xlstore', 'usercategories'),
(22, 'xlstore', 'userfollow'),
(15, 'xlstore', 'usernotifications'),
(46, 'xlstore_ecommerce', 'ec_companymobile'),
(45, 'xlstore_ecommerce', 'ec_companysettings'),
(42, 'xlstore_ecommerce', 'ec_marketaccess'),
(43, 'xlstore_ecommerce', 'ec_shoppingcart'),
(44, 'xlstore_ecommerce', 'ec_shoppingcartitems'),
(30, 'xlstore_managment', 'ms_companyadministrator'),
(47, 'xlstore_managment', 'ms_companymobile'),
(38, 'xlstore_managment', 'ms_companyteller'),
(29, 'xlstore_managment', 'ms_licencekey'),
(35, 'xlstore_managment', 'ms_licencekeyactivations'),
(34, 'xlstore_managment', 'ms_marketaccess'),
(41, 'xlstore_managment', 'ms_marketsales'),
(40, 'xlstore_managment', 'ms_marketsalesdetails'),
(28, 'xlstore_managment', 'ms_productentry'),
(26, 'xlstore_managment', 'ms_receiptdetails'),
(27, 'xlstore_managment', 'ms_receipts'),
(33, 'xlstore_managment', 'ms_settings');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2017-08-06 05:42:51.289000'),
(2, 'auth', '0001_initial', '2017-08-06 05:43:00.861000'),
(3, 'admin', '0001_initial', '2017-08-06 05:43:04.084000'),
(4, 'admin', '0002_logentry_remove_auto_add', '2017-08-06 05:43:04.151000'),
(5, 'contenttypes', '0002_remove_content_type_name', '2017-08-06 05:43:05.990000'),
(6, 'auth', '0002_alter_permission_name_max_length', '2017-08-06 05:43:06.912000'),
(7, 'auth', '0003_alter_user_email_max_length', '2017-08-06 05:43:07.753000'),
(8, 'auth', '0004_alter_user_username_opts', '2017-08-06 05:43:07.804000'),
(9, 'auth', '0005_alter_user_last_login_null', '2017-08-06 05:43:08.206000'),
(10, 'auth', '0006_require_contenttypes_0002', '2017-08-06 05:43:08.240000'),
(11, 'auth', '0007_alter_validators_add_error_messages', '2017-08-06 05:43:08.361000'),
(12, 'auth', '0008_alter_user_username_max_length', '2017-08-06 05:43:09.088000'),
(13, 'sessions', '0001_initial', '2017-08-06 05:43:09.680000'),
(14, 'xlstore', '0001_initial', '2017-08-06 05:43:52.357000'),
(15, 'xlstore_managment', '0001_initial', '2017-08-06 05:44:00.125000'),
(16, 'xlstore_managment', '0002_auto_20170806_1815', '2017-08-06 15:15:22.795000'),
(17, 'xlstore_managment', '0003_ms_productentry_item_price', '2017-08-08 12:42:22.932000'),
(18, 'xlstore_managment', '0004_ms_receiptdetails_item_price', '2017-08-08 12:52:55.934000'),
(21, 'xlstore_managment', '0005_auto_20170808_1632', '2017-09-12 04:57:24.621000'),
(26, 'xlstore', '0002_auto_20170914_1957', '2017-09-14 17:03:50.765000'),
(31, 'xlstore_managment', '0006_auto_20170823_1632', '2017-10-06 09:06:01.665000'),
(32, 'xlstore_managment', '0007_auto_20170914_1957', '2017-10-06 09:06:01.772000'),
(33, 'xlstore_managment', '0008_auto_20171006_1212', '2017-10-06 09:13:31.400000'),
(34, 'xlstore_managment', '0009_auto_20171009_1759', '2017-10-09 15:01:15.061000'),
(35, 'xlstore_managment', '0010_auto_20171010_1003', '2017-10-10 07:04:25.483000'),
(36, 'xlstore_managment', '0011_auto_20171012_0914', '2017-10-12 06:15:54.294000'),
(37, 'xlstore_managment', '0012_auto_20171015_1718', '2017-10-15 14:19:26.859000'),
(38, 'xlstore_managment', '0013_auto_20171028_0710', '2017-10-28 04:14:19.416000'),
(39, 'xlstore', '0003_companycategories', '2017-11-09 04:24:43.654000'),
(40, 'xlstore_managment', '0014_auto_20171109_0723', '2017-11-09 04:24:43.695000'),
(41, 'xlstore', '0004_auto_20171109_0744', '2017-11-09 04:45:18.706000'),
(42, 'xlstore_managment', '0015_auto_20171109_0744', '2017-11-09 04:45:18.724000'),
(43, 'xlstore', '0005_auto_20180116_1420', '2018-01-16 14:22:30.598741'),
(44, 'xlstore_managment', '0016_auto_20180116_1420', '2018-01-16 14:22:30.654539'),
(45, 'xlstore', '0006_companycategories_image', '2018-01-20 04:34:00.808837'),
(46, 'xlstore_managment', '0017_auto_20180120_0432', '2018-01-20 04:34:00.927067'),
(47, 'xlstore', '0007_auto_20180120_0442', '2018-01-20 04:43:46.397107'),
(48, 'xlstore_managment', '0018_auto_20180120_0442', '2018-01-20 04:43:46.482756'),
(49, 'xlstore_managment', '0019_auto_20180122_0252', '2018-01-22 02:54:40.826713'),
(50, 'xlstore_managment', '0020_auto_20180122_0334', '2018-01-22 03:34:54.012106'),
(51, 'xlstore_managment', '0021_auto_20180122_0557', '2018-01-22 05:58:23.464839'),
(52, 'xlstore', '0008_auto_20180211_1743', '2018-02-11 17:50:58.359637'),
(53, 'xlstore_managment', '0022_auto_20180211_1743', '2018-02-11 17:50:58.415465'),
(54, 'xlstore_managment', '0023_auto_20180220_0355', '2018-02-20 03:56:56.391124'),
(55, 'xlstore_managment', '0024_auto_20180224_1556', '2018-02-24 15:57:43.895723'),
(56, 'xlstore_managment', '0025_auto_20180225_1527', '2018-02-25 15:28:48.024668'),
(57, 'xlstore_ecommerce', '0001_initial', '2018-02-25 15:43:14.803588'),
(58, 'xlstore_managment', '0026_auto_20180225_1542', '2018-02-25 15:43:14.859322'),
(59, 'xlstore_ecommerce', '0002_auto_20180225_1629', '2018-02-25 16:30:48.684975'),
(60, 'xlstore_managment', '0027_auto_20180225_1629', '2018-02-25 16:30:48.765387'),
(61, 'xlstore_ecommerce', '0003_auto_20180226_0122', '2018-02-26 01:23:49.099554'),
(62, 'xlstore_managment', '0028_auto_20180226_0122', '2018-02-26 01:23:49.279982'),
(63, 'xlstore_ecommerce', '0004_auto_20180226_0137', '2018-02-26 01:38:18.255551'),
(64, 'xlstore_managment', '0029_auto_20180226_0137', '2018-02-26 01:38:18.333267'),
(65, 'xlstore_ecommerce', '0005_auto_20180226_0521', '2018-02-26 05:22:39.415794'),
(66, 'xlstore_managment', '0030_auto_20180226_0521', '2018-02-26 05:22:50.694804'),
(67, 'xlstore_ecommerce', '0006_auto_20180301_1620', '2018-03-01 16:21:02.231575'),
(68, 'xlstore_managment', '0031_auto_20180301_1620', '2018-03-01 16:21:02.276486'),
(69, 'xlstore_ecommerce', '0007_auto_20180301_1639', '2018-03-01 16:40:22.183987'),
(70, 'xlstore_managment', '0032_auto_20180301_1639', '2018-03-01 16:40:22.265271'),
(71, 'xlstore_ecommerce', '0008_auto_20180301_1809', '2018-03-01 18:11:11.708312'),
(72, 'xlstore_managment', '0033_auto_20180301_1809', '2018-03-01 18:11:12.184344'),
(73, 'xlstore_ecommerce', '0009_auto_20180302_0422', '2018-03-02 04:24:03.654706'),
(74, 'xlstore_managment', '0034_auto_20180302_0422', '2018-03-02 04:24:03.732756'),
(75, 'xlstore_ecommerce', '0010_ec_companysettings_use_paypal', '2018-03-02 05:07:17.868179'),
(76, 'xlstore_managment', '0035_auto_20180302_0506', '2018-03-02 05:07:18.029319'),
(77, 'xlstore_ecommerce', '0011_auto_20180303_0223', '2018-03-03 02:24:25.600414'),
(78, 'xlstore_managment', '0036_auto_20180303_0223', '2018-03-03 02:24:27.894064'),
(79, 'xlstore_managment', '0037_auto_20180303_0246', '2018-03-03 02:47:02.342418'),
(80, 'xlstore_ecommerce', '0012_ec_shoppingcart_finished_date', '2018-03-03 17:06:13.859587'),
(81, 'xlstore_managment', '0038_auto_20180303_1705', '2018-03-03 17:06:14.081520');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('03o378140r08zujcai1ijevqynntllmf', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-03 12:24:35.778105'),
('0c2bnh8xonawzdy2uwwmwqb97cgvztdd', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 17:51:26.956000'),
('0f3gq0m93nue3xirxxu6xwgc9tph84vh', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 05:57:34.172000'),
('0kbynsgekc4qdculsoitwo4km6zcpyi6', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 11:59:29.073000'),
('0uucb879sushi3lq3og6mbtotjri8gdd', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 06:52:54.574000'),
('11aj34i3daf5v6u2m1jactzjo1arv11k', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:26:35.815000'),
('147nyqcbuwr6xxsouimlytpqmb1xywk6', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 08:45:07.886000'),
('1yo06zupurow62ifm7b5hjf57la6ejow', 'OWJjMmVlOTZlOGFlZTc3OWU1ZGIzZTkzM2I0OWY3MmM5YjFlZjc1MTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiYWRtaW4iOiJhZG1pbiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY29tcGFueV9uYW1lIjoiQ2hyaXNjb3RUZWNoSW5jIiwibXMiOjEsInBrIjoxLCJfYXV0aF91c2VyX2hhc2giOiJhMjQ4ZmFiMjFmOGY5N2YxOWE0MTc2OWEyM2Q5ZTA3NWE1Mzc1ODllIiwiY29tcGFueV9lbWFpbCI6ImlyY2hyaXN0aWFuc2NvdHRAZ21haWwuY29tIn0=', '2018-03-19 05:16:57.299149'),
('1yq5x701f7k3fgps978vsi44aafxjh5l', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-17 07:33:43.862000'),
('20aj6cuau3weoernow496mc6llvio115', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-24 17:38:56.482259'),
('23v2xza1wtz2noupdomzwvkit0rq56d7', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-02 05:37:40.440214'),
('2j9qef2zdc85xwhlkigfedq2lsaaiqr7', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:29:52.296000'),
('2r6v8a27wqauurlbckkbfjd09kwgo0ue', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2017-09-28 12:19:04.651000'),
('2srgogofl4yyuc2pw6cf7h02j56xv0sd', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-12-20 13:49:15.581000'),
('2tamzs73zpea95h40i9xlo9nshv9pwgx', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-14 05:42:10.825347'),
('2xoh7g6f90nqrjgoqegjpiawfbcltj9d', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-14 06:01:02.121000'),
('38hn7kiqxqkh19ptmhhyd4osnxfn98gz', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 05:55:05.830000'),
('3f3dm5fdw8u338rngt110564e361nfzc', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-23 10:07:51.305000'),
('3kd3bm7wybhj5qww5zggaelu5okkmf4v', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 05:14:46.218000'),
('3m8jrl1sgxx2qg57bq4p6yabp8katmf6', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-10-17 13:45:33.031000'),
('3oz2i9jg76p1jz117njgqv772l7mjhgh', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 05:57:45.509000'),
('3tswsw2qumhyiuerb09vimq4a0ashk6j', 'MTU1NzhhNWY5YmZmM2JlY2UwNjJlYjJlYzIyYzRhMzRlMTRiZTEwZDp7ImFkbWluIjoiYWRtaW4iLCJwayI6MiwiY29tcGFueV9lbWFpbCI6Imhvc2FuYXRleHRpbGVAZ21haWwuY29tIiwibXMiOjIsImNvbXBhbnlfbmFtZSI6Ikhvc2FuYVRleHRpbGUifQ==', '2017-09-28 12:25:48.288000'),
('45tgde5omc9b0b7f5awfxwkbg8x44lrn', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-17 11:51:27.533000'),
('4hruznnrqc63g5dmr6as3shdjpgpmryy', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2017-12-04 06:15:42.350000'),
('5454ymtebvd03l7z4w6p77yggzn69pqz', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-09-04 13:39:24.340000'),
('5drb954jgzzr46wevy1uidm7q3e40nh1', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-13 13:13:27.634245'),
('5n115hds77ffpkbjzfxj82flo875sbp1', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 06:06:55.461000'),
('5tngkh0nn1xid6jfi3cj1jdotfsw5myc', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:03:11.671000'),
('6bbwfvcghcuguojszh1b87yasa18s8kb', 'MGEwNmNlY2FmODA2YWZiYzdlNTZiYjMzMDFlODRlYzM4YmQyYmRhMjp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwiY29tcGFueV9lbWFpbCI6ImlyY2hyaXN0aWFuc2NvdHRAZ21haWwuY29tIiwidXNlciI6Mn0=', '2018-01-26 07:54:51.043457'),
('6hjta65rqkj7ob4gsfopyv6oem7jzn8q', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 13:30:25.794000'),
('73fpdvcbaym5jyyqqxadgxthruf9nach', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 06:21:07.565000'),
('73popkrgky02jsdtikmukgr0xq6pii2c', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2017-12-04 06:24:53.786000'),
('7dwpq9u3a8eoabe6b95d5gcyo5golg86', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-20 06:42:33.018000'),
('7pm78kk6lmkzk33vbib2c7hsw243b8qk', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2018-01-31 14:18:37.082613'),
('7xnln9r3q000r6r4d9coijsk03hj1kym', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 19:33:13.999000'),
('86mciyawxp2bcb20jhqrq9k0del6jvsk', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 05:15:56.045000'),
('89h3jtql0lrdej46j9h5kmawq4yscfvj', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-09-08 06:17:10.951000'),
('8be775om7ot407tvobytune5hzb4m0c1', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 16:41:45.371000'),
('9ic85xj5du4k1cxfu5vveu8f84niipuw', 'NWEwYjAxZjIzYzdhNmM3ZWUyN2I4YjJhYjFlMDZjM2VmNjY5MDUyOTp7fQ==', '2018-02-02 02:43:20.035651'),
('9n8saumo6f8l4nc5pb9fs1oprw4yaslj', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2018-02-01 14:12:08.042996'),
('9sjez6feepo6g9hvhuzw1zhzwahkpc5n', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 06:35:11.704000'),
('9u983bd0v6vchgdhdoxn7kuykmfucsyv', 'NDEzNWY3YmU3NDY0NjViNWY0MmI0M2NkZDc1YmY1MmU1Yjg2ZDhiNzp7ImFkbWluIjoiYWRtaW4iLCJjb21wYW55X25hbWUiOiJjaHJpc2NvdHRlY2guaW5jIiwibXMiOjEsInBrIjoxLCJjb21wYW55X2VtYWlsIjoiaXJjaHJpc3RpYW5zY290dEBnbWFpbC5jb20ifQ==', '2018-01-01 06:18:11.380000'),
('a17ls8h4gdikvftnfp9jwe82rtbflpjq', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:15:19.019000'),
('a8izjdpulh6m77dp1afsmx4rv04dn9yg', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 05:44:46.544000'),
('ae70v75rh8pj7aksh0zgijyfg9k3ug48', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 06:05:46.937000'),
('at4xldxzv2ornp2ltohmxk15e728o6bz', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2017-12-04 06:21:27.619000'),
('c5mekmahvo7hx2sxxxishj4o6jweuybl', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-14 04:42:59.111040'),
('cgc8lhpm4gn6j63ywd4ouaim1w7rtfta', 'MDViMGJmOTZiMGVlNDUyZWUwMDE2ZDIxZDlhOTY1NzBjNzU1MzEwZjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiYWRtaW4iOiJhZG1pbiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY29tcGFueV9uYW1lIjoiQ2hyaXNjb3RUZWNoSW5jIiwibXMiOjEsInBrIjoxLCJfYXV0aF91c2VyX2hhc2giOiJjZmVlMGM4MjZlMTliOGQ0NTQwYmQ1OGE3ZGUxMmQ5NWZiNmIzMjU1IiwiY29tcGFueV9lbWFpbCI6ImlyY2hyaXN0aWFuc2NvdHRAZ21haWwuY29tIn0=', '2018-02-25 06:15:29.902243'),
('ck4ws7f1tc5mi6i751u9b8glg6qowjmd', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-01-31 07:10:20.802082'),
('clk0cl0leqwj238t7fjnw02umwr7z4ji', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 08:44:26.853000'),
('cpwem39vfxf5qf2yiin9swje1m7vh3lc', 'NTc0OTM4MTM3ODdhYWY2MDMwNWUzZTE1ZDRhMTNjYTE0Nzg3MWUwYjp7InBrIjoxLCJjb21wYW55X2VtYWlsIjoiaXJjaHJpc3RpYW5zY290dEBnbWFpbC5jb20iLCJjb21wYW55X25hbWUiOiJjaHJpc2NvdHRlY2guaW5jIn0=', '2018-01-26 06:23:39.597819'),
('cspobnuvdmbzait6yucbcai4bidvbzii', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:36:30.720000'),
('d81qg5ozdxalt6l0l61c1j3xlymozrho', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 05:58:20.737000'),
('ddtekddcnrl3fqbo097njkc5oxcgfrdq', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 06:40:15.792000'),
('dh3nbs5d1xc2jmhkhv1qoo0qbuqfg4zc', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-23 16:33:38.957000'),
('drp4818gedk82lyi1vkhtk51frxupiwk', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-14 15:23:33.576304'),
('eneoltvg34xhow7s48071prmd1c6qbs6', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-11 13:47:35.828757'),
('f45tvqlbiriiwzcld48217v7oh2y04qz', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:38:16.955000'),
('f7aew8ctmrxjwev1lj50eanjqdri8zn2', 'YWY3NmQ0NDk0ZTI0YTkyZTZlYzg2YjM5ZTkxMGU1NjYyNzhkMjFjOTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiYWRtaW4iOiJhZG1pbiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY29tcGFueV9uYW1lIjoiY2hyaXNjb3R0ZWNoLmluYyIsIm1zIjoxLCJwayI6MSwiX2F1dGhfdXNlcl9oYXNoIjoiM2I3MjhjOTIxMDhmMzZmYmY1NGMxZTQ0YzllMDAxODg2MzEzNTNhNiIsImNvbXBhbnlfZW1haWwiOiJpcmNocmlzdGlhbnNjb3R0QGdtYWlsLmNvbSJ9', '2017-11-05 05:01:45.594000'),
('f8kcuiz94iturm03k3dnz3rketptoaeo', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 13:32:37.490000'),
('fn0hkk6ceglhl4bhm57inx4cvkfgx1fr', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-13 18:49:03.386355'),
('fpk4vmd1ibthgx3kgxbglg38xg7fu5sw', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 06:40:47.662000'),
('fvwhg9yaa23sididbdohhf7vy90um9ms', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:47:17.066000'),
('fya4u2bxzqvqbyb25wzmtwemig8rg7af', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 05:59:14.497000'),
('gce7hc8xa7p3e9urn1l68dmcaxq0gjb8', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-14 09:57:29.491403'),
('ggnb6oyqvqmj1dnzmm6glj3chl6z6he0', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:55:49.970000'),
('gnv81csjrmuxsjk0vuwd0209b18uvvqw', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 06:02:22.897000'),
('go5ouyllz8velnogbtfnpyl2n34wii4l', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-17 09:35:59.010000'),
('h0i76gaaddnueflrjzq6hbkxdowoed0h', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-17 11:56:00.074000'),
('h1hgf2whszp8msbl33v5xr2v36t8q07i', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-14 15:04:53.343345'),
('hd64icfbr2owqkaz9ev4d10md3azrkme', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-23 10:17:42.595000'),
('hp0rvpwu1eimfjga0vumxug2t7eiwsv6', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 05:49:26.963000'),
('ihw6bh54me3g7ho1fi1f3x3zh55e9tcb', 'MTU1NzhhNWY5YmZmM2JlY2UwNjJlYjJlYzIyYzRhMzRlMTRiZTEwZDp7ImFkbWluIjoiYWRtaW4iLCJwayI6MiwiY29tcGFueV9lbWFpbCI6Imhvc2FuYXRleHRpbGVAZ21haWwuY29tIiwibXMiOjIsImNvbXBhbnlfbmFtZSI6Ikhvc2FuYVRleHRpbGUifQ==', '2018-03-20 03:40:04.133733'),
('iimskpcsiqjzw7pj8v05t8j7dweaoytj', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2018-02-01 06:08:26.796174'),
('ij64i4gg991dbz1yklqn5oyell2364az', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 09:41:30.697000'),
('j16c5q1nbaor642nzogamh5da9rk7vsh', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-04 13:30:00.721880'),
('ja31tuy8f5vxlx03akknae0q9nxldmgq', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-20 04:33:12.067000'),
('k3el6ro4jqn4h29cfbftuczn9zzpvn69', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-27 04:36:55.658000'),
('kcajpydwaygy0j2fadkngof9qg2ez3a1', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:07:43.205000'),
('kipngn4x3pm50vt86kg0z89t5d3hqhxn', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-15 07:07:48.214207'),
('kofc0tve9jl5vtgxl3wyscez1ppa0gfm', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 06:05:29.575000'),
('kr4dg3w2ok170c0awf38mgk6loms3eyg', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-01-27 20:36:20.654310'),
('l71n4pk0zsl88qwgvykk4nsm7petayij', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2018-02-01 05:12:44.108421'),
('lhcr6afv3zhzhx3q0fsql6nuzg1uqv0x', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-01-27 20:30:58.816245'),
('luytx3l0gx1t64eykgg0hcol3dui7xd9', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 08:43:52.136000'),
('lwpkc10ns1e68ch8jf6z8m196auemrdd', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-13 10:02:57.746068'),
('ly8qln03kh7qijlla7r6bx0n23s1rte4', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 13:40:38.316000'),
('n6o541bxgz1eg5emcfvjb9idxf76vmrv', 'NWEwYjAxZjIzYzdhNmM3ZWUyN2I4YjJhYjFlMDZjM2VmNjY5MDUyOTp7fQ==', '2018-02-09 08:33:52.303511'),
('nbff8yq82xpd0mzpj14f65kl0fz09poi', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:07:47.746000'),
('ojxm4fr25ca17lk2ntgjgtlvpbuwi8vk', 'NDk0NmVjY2JkYjFiMmZkNWZkMjYzNmY4ZjVhOWY5YjlmMzQ2NzNkYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiYWRtaW4iOiJhZG1pbiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY29tcGFueV9uYW1lIjoiY2hyaXNjb3R0ZWNoLmluYyIsIm1zIjoxLCJwayI6MSwiX2F1dGhfdXNlcl9oYXNoIjoiNDBiMzdhMmNmNzJiZjExZGFjODczYzczNGJlYzAwOTgyY2JhMzRhYSIsImNvbXBhbnlfZW1haWwiOiJpcmNocmlzdGlhbnNjb3R0QGdtYWlsLmNvbSJ9', '2017-10-25 17:00:48.179000'),
('otiv9z2te4jbo0fcan6zzc89np4lnnyp', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2018-01-28 21:44:10.046733'),
('pbqn1epp8h9jru7hgctkh8jnk5w5riv3', 'MjQwZTc5NDA5OGVlNTAyZTMyYWUzOGY1MmMyODM3NTIzY2QzMmFlZDp7ImFkbWluIjoiYWRtaW4iLCJwayI6MSwiY29tcGFueV9lbWFpbCI6ImlyY2hyaXN0aWFuc2NvdHRAZ21haWwuY29tIiwibXMiOjEsImNvbXBhbnlfbmFtZSI6ImNocmlzY290dGVjaC5pbmMifQ==', '2018-01-20 21:06:57.954350'),
('peyxdfvu1mgki0sviyhgmoqnflbq2vfr', 'MzQ2YzA4OWFlN2Y0NWUyYWNiMjdhYTI4NTYxMWQ4NGFiZGFiZDZjNTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJjb21wYW55X2VtYWlsIjoiaXJjaHJpc3RpYW5zY290dEBnbWFpbC5jb20iLCJ1c2VyIjoxfQ==', '2017-08-21 06:12:17.124000'),
('pisqkk900bkxad8em89ku36yuc1dj77b', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 13:21:26.696000'),
('ps4qr0mpi1fpckl4h32wxtgbptfzup05', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:42:11.395000'),
('pxe11koy15braa0czk8cp76z90uleivx', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 13:32:38.509000'),
('py7q0np3rjaustgus8ws9nggtkv5dtk9', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-12-04 06:24:22.729000'),
('q4dqvaqhp6l89ylj9l7dajy5i1576afv', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 06:03:29.121000'),
('q7710361zdk4ju8n46iym2vsfpjhotgh', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 05:50:27.380000'),
('qkyckcg7rvq5wakjzqxju0dj4nt1f2e2', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 12:36:59.380000'),
('qm7a36pg5uapmh1eea6fagxa7r5y04ri', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-09-19 13:07:17.096000'),
('qrm0ygi27r15wgv0gspb1pw9baedfti4', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 06:10:51.375000'),
('qzgt493wxqwde8u8wicf5l2b0h2ocgl4', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:32:34.197000'),
('r99v0gcpcu5ba0r8a1tx3gvel4fexlou', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 12:45:13.614000'),
('rubqis8xbram887sl1ft9ektke2xusrj', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-12-04 06:26:28.466000'),
('s7uzdik79cfdrlafxpztmr6gh75umm2d', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-14 06:53:21.922253'),
('sj3jjlm5j03ovcz3c5cq5jwhllzeq0nf', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-05 05:10:18.532628'),
('ss670lberqdph375xbijmpr38ra1a0ap', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:18:40.141000'),
('ssudj5shao4l3l7cvvvpcnsy4u2zj6xe', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-20 04:32:24.032000'),
('sxwpjexnqp9r62qbrmzwupmwhc8nq499', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2018-01-29 10:59:23.737114'),
('t1evqtnu0jx39ta0s0jd7fy1jr59097n', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 14:54:08.372000'),
('t9y37c73o8d72htjgngrfjzxay7md883', 'NDlkYTcwNGMxZGRmN2E4YjJkZmVlZWIwNWI1NWU5ODVlY2JhNTdiNTp7ImFkbWluIjoiYWRtaW4iLCJjb21wYW55X25hbWUiOiJIb3NhbmFUZXh0aWxlIiwibXMiOjIsInBrIjoyLCJjb21wYW55X2VtYWlsIjoiaG9zYW5hdGV4dGlsZUBnbWFpbC5jb20ifQ==', '2017-10-25 12:28:17.590000'),
('tqmojj4k1t564hb9ctepvz3oz8mfzu5e', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-01-27 05:19:52.679476'),
('tzvo62l7blpdtkasyanorvwygcwu1pey', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-02-14 07:22:28.100691'),
('ugiouaaihk7l7nu7kngkxx2iqhid000l', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-12-03 05:57:12.554000'),
('ujb4i0g613w2oczpr3x7diz4ad5md9hq', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 07:00:57.405000'),
('ume9h9rpew5dfuq4hldtmtl0k2gnzohb', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 05:17:40.422000'),
('up0lduegwotsyvwi2e9aq1j7ujc5c50r', 'Nzg5N2E3Zjc1ODNhMjAwN2JhYTMyYzM5ZjIxMWQ5YTk3NzM3NjgwOTp7InVzZXJuYW1lIjoiUHJpbmNlc3NlIiwidXNlciI6Mn0=', '2017-12-04 06:19:59.299000'),
('vympn0d1xbmawmzm1q3b8mfii6dpzpz2', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2018-03-17 05:51:02.641089'),
('wm2jvcxa0u4k6iycn1bf6v7rew0x9fp1', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 12:00:38.553000'),
('wq2xvxc71ffy2678zwaiz1dsyfc034p2', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 17:31:12.010000'),
('x4bev5next848rox51hirlkyqmzg1mv6', 'YWY3NmQ0NDk0ZTI0YTkyZTZlYzg2YjM5ZTkxMGU1NjYyNzhkMjFjOTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiYWRtaW4iOiJhZG1pbiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY29tcGFueV9uYW1lIjoiY2hyaXNjb3R0ZWNoLmluYyIsIm1zIjoxLCJwayI6MSwiX2F1dGhfdXNlcl9oYXNoIjoiM2I3MjhjOTIxMDhmMzZmYmY1NGMxZTQ0YzllMDAxODg2MzEzNTNhNiIsImNvbXBhbnlfZW1haWwiOiJpcmNocmlzdGlhbnNjb3R0QGdtYWlsLmNvbSJ9', '2017-12-07 04:59:14.932000'),
('y3y4jhj5xncojmnwx8iyepypq0bw6hsu', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 13:26:45.003000'),
('ytj1gnhr1c2pb263xuif19lz9800s2aa', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-18 08:42:43.724000'),
('yuvaqr92oie313h8kkz0798z9ncxhf2a', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-09-08 07:34:15.942000'),
('yxlyzqgmb38akyg5lyqqzm2p0nduicyo', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:37:46.428000'),
('z0xcboty0hz9zciftokq4dj17265reuc', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-20 04:36:03.512000'),
('z15o6ox48c4kw1s7nsc1fo8v9q86dips', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-17 10:28:01.055000'),
('z9ui9zslj20zb5w31t7izsvwlwl0ske8', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-12-03 05:54:09.672000'),
('znvi57d5t6y8vx8w3ovh68d101a895a6', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-12-12 06:34:00.405000'),
('zpt0p1ilgzm3jxkivlc99cxh5j32s1ob', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-16 05:57:21.891000'),
('zqtsjzjob9ccfhlvic2gfvoxdidx07s8', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:36:17.894000'),
('zw94xro3z5er0anb180sipjo9czar8pa', 'NzhiNTVmMzI5MDJmOGQ0YThjMzJhZjM5MzM1MzEyZGRlYzdlMzZhMTp7InVzZXJuYW1lIjoiSXJDaHJpc2NvdHQiLCJ1c2VyIjoxfQ==', '2017-11-19 14:06:52.149000');

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_address`
--

CREATE TABLE `xlstore_address` (
  `added_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `address` varchar(255) NOT NULL,
  `latitude` decimal(20,10) NOT NULL,
  `longitude` decimal(20,10) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_address`
--

INSERT INTO `xlstore_address` (`added_date`, `id`, `address`, `latitude`, `longitude`, `company_id`, `user_id`) VALUES
('2018-02-13 14:10:23.785708', 1, 'Kampala Serena Hotel, Kampala, Uganda', '0.3192456000', '32.5864363000', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_advertisments`
--

CREATE TABLE `xlstore_advertisments` (
  `posted_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `video` varchar(100) NOT NULL,
  `advertisment_text` longtext NOT NULL,
  `company_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_advertisments`
--

INSERT INTO `xlstore_advertisments` (`posted_date`, `id`, `video`, `advertisment_text`, `company_id`, `product_id`) VALUES
('2017-08-18 08:27:30.831000', 1, 'advertisments/2017/08/18/scott_031.mp4', '<p>sdhsydggda</p>', 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_categories`
--

CREATE TABLE `xlstore_categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `created_date` datetime(6) NOT NULL,
  `company_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_categories`
--

INSERT INTO `xlstore_categories` (`id`, `name`, `description`, `created_date`, `company_id`) VALUES
(1, 'Computers', 'Best computers for all brands, prices and qualities at the best price and warrant.', '2017-08-06 05:47:24.579000', 1),
(2, 'Mobile Phones', 'Best brand new and second hand mobile phones for all brands, price and qualities', '2017-08-06 05:47:24.579000', 1),
(3, 'Tissus', 'On vends toute sorte de tissue de couture', '2017-09-14 12:02:07.542000', 2);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_company`
--

CREATE TABLE `xlstore_company` (
  `id` int(11) NOT NULL,
  `name` varchar(250) NOT NULL,
  `name_dotted` varchar(250) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(20) NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `cover_image` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `country` varchar(2) DEFAULT NULL,
  `town` varchar(250) DEFAULT NULL,
  `motto` longtext,
  `description` longtext,
  `is_authenticated` tinyint(1) NOT NULL,
  `registration_date` datetime(6) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `has_seen_tutorial` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_company`
--

INSERT INTO `xlstore_company` (`id`, `name`, `name_dotted`, `email`, `password`, `profile_image`, `cover_image`, `phone_number`, `country`, `town`, `motto`, `description`, `is_authenticated`, `registration_date`, `category_id`, `has_seen_tutorial`) VALUES
(1, 'ChriscotTech Inc', 'ChriscotTechInc', 'irchristianscott@gmail.com', 'chriscons', 'company_profile/1502013226_14_storks_3.jpg', 'company_cover/1502013252_52_wallpaper.jpg', '+256756891594', 'UG', 'Kampala', 'Best Tech Support Ever', '', 0, '2017-08-06 09:52:00.409000', 3, 0),
(2, 'Hosana Textile', 'HosanaTextile', 'hosanatextile@gmail.com', 'oneschance', '', '', '+243853097280', 'CD', 'Goma', NULL, NULL, 0, '2017-09-14 12:13:10.802000', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_companycategories`
--

CREATE TABLE `xlstore_companycategories` (
  `id` int(11) NOT NULL,
  `name` varchar(250) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_companycategories`
--

INSERT INTO `xlstore_companycategories` (`id`, `name`, `description`, `image`) VALUES
(1, 'Fashion', 'Every Thing That concerns fashion like clothes, shoes, and others', 'admin/categories/fashion.png'),
(2, 'Beauty', 'Every Thing that concerns beauty like make up, oil, perfume and others', 'admin/categories/beauty.png'),
(3, 'Electronic', 'Every thing that can work with electricity like TV, Mobile Phone, Computers and others', 'admin/categories/electronic.png'),
(4, 'Furniture', 'Every thing that concerns things that can be used in the house', 'admin/categories/fourniture.png'),
(5, 'Stationary', 'Every thing that can be used in an office', 'admin/categories/stationary.png'),
(6, 'Mechanical', 'Every thing that concerns cars, motorbikes, bicycles and others', 'admin/categories/mechanical.png'),
(7, 'House & Appartement', 'Every thing concerning places where people can live', 'admin/categories/houses.png'),
(8, 'Hardware', 'Every thing that concerns construction materials', 'admin/categories/hardware.png'),
(9, 'Music', 'Every thing that involves music', 'admin/categories/music.png'),
(10, 'Others', '...', 'admin/categories/others.png'),
(11, 'Discotec', 'Every thing that concerns visual and/or audio output', 'admin/categories/discotec.png'),
(12, 'Grocery', 'Everything that concerns food and others important necessities', 'admin/categories/grocery.png'),
(13, 'Library', 'Everything that concern reading (books, newspapers and others)', 'admin/categories/library.png'),
(14, 'Medicinal', 'Everything that concerns medicine and all curative products', 'admin/categories/medicine.png'),
(15, 'Restaurants & Bars', 'Everything that concerns eating and drinking', 'admin/categories/restaurant.png');

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_companynotifications`
--

CREATE TABLE `xlstore_companynotifications` (
  `posted_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `notification_id` int(11) NOT NULL,
  `about` varchar(200) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `concern_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_companynotifications`
--

INSERT INTO `xlstore_companynotifications` (`posted_date`, `id`, `notification_id`, `about`, `is_read`, `concern_id`, `user_id`) VALUES
('2017-08-23 04:38:17.454000', 1, 4, 'interess', 0, 1, 1),
('2017-08-23 04:38:27.051000', 2, 3, 'interess', 0, 1, 1),
('2017-08-25 13:28:07.994000', 3, 6, 'interess', 0, 1, 1),
('2017-09-14 12:34:31.605000', 4, 4, 'interess', 0, 1, 2),
('2017-09-14 15:20:59.966000', 5, 5, 'like_comment', 0, 1, 1),
('2017-09-14 15:21:12.519000', 6, 5, 'like_comment', 0, 1, 2),
('2017-10-05 04:42:40.419000', 7, 4, 'comment', 0, 1, 1),
('2017-11-06 05:57:07.140000', 8, 1, 'comment', 0, 1, 1),
('2018-01-10 07:44:28.241611', 9, 1, 'follow', 0, 1, 1),
('2018-01-10 18:16:04.212996', 10, 1, 'follow', 0, 2, 1),
('2018-01-15 10:41:55.178815', 11, 9, 'interess', 0, 2, 2),
('2018-01-15 10:42:09.435334', 12, 8, 'interess', 0, 2, 2),
('2018-01-15 10:42:09.576213', 13, 8, 'interess', 0, 2, 2),
('2018-01-18 04:55:49.883274', 14, 10, 'reply', 0, 1, 1),
('2018-03-01 04:24:17.678401', 17, 10, 'like_product', 0, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_ecommerce_ec_companysettings`
--

CREATE TABLE `xlstore_ecommerce_ec_companysettings` (
  `id` int(11) NOT NULL,
  `use_ecommerce` tinyint(1) NOT NULL,
  `paypal` varchar(200) DEFAULT NULL,
  `mobile` tinyint(1) NOT NULL,
  `company_id` int(11) NOT NULL,
  `use_paypal` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_ecommerce_ec_companysettings`
--

INSERT INTO `xlstore_ecommerce_ec_companysettings` (`id`, `use_ecommerce`, `paypal`, `mobile`, `company_id`, `use_paypal`) VALUES
(1, 0, 'irchristianscott@gmail.com', 0, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_ecommerce_ec_marketaccess`
--

CREATE TABLE `xlstore_ecommerce_ec_marketaccess` (
  `time_from` datetime(6) DEFAULT NULL,
  `time_to` datetime(6) DEFAULT NULL,
  `key_date` date NOT NULL,
  `id` int(11) NOT NULL,
  `key` varchar(100) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `access_time` int(11) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_ecommerce_ec_marketaccess`
--

INSERT INTO `xlstore_ecommerce_ec_marketaccess` (`time_from`, `time_to`, `key_date`, `id`, `key`, `status`, `access_time`, `company_id`, `user_id`) VALUES
(NULL, NULL, '2018-02-25', 1, 's48RBo4K', 'vip', NULL, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_ecommerce_ec_shoppingcart`
--

CREATE TABLE `xlstore_ecommerce_ec_shoppingcart` (
  `saved_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `status` varchar(100) NOT NULL,
  `total_paid` decimal(18,2) NOT NULL,
  `market_id` int(11) NOT NULL,
  `others_chargers` decimal(18,2) NOT NULL,
  `total_net` decimal(18,2) NOT NULL,
  `delivery` tinyint(1) NOT NULL,
  `payment_mode` varchar(30) DEFAULT NULL,
  `finished_date` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_ecommerce_ec_shoppingcart`
--

INSERT INTO `xlstore_ecommerce_ec_shoppingcart` (`saved_date`, `id`, `status`, `total_paid`, `market_id`, `others_chargers`, `total_net`, `delivery`, `payment_mode`, `finished_date`) VALUES
('2018-02-26 02:05:31.330389', 1, 'suspended', '0.00', 1, '0.00', '0.00', 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_ecommerce_ec_shoppingcartitems`
--

CREATE TABLE `xlstore_ecommerce_ec_shoppingcartitems` (
  `saved_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `item_price` decimal(18,2) DEFAULT NULL,
  `total` decimal(18,2) NOT NULL,
  `product_id` int(11) NOT NULL,
  `cart_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_ecommerce_ec_shoppingcartitems`
--

INSERT INTO `xlstore_ecommerce_ec_shoppingcartitems` (`saved_date`, `id`, `quantity`, `item_price`, `total`, `product_id`, `cart_id`) VALUES
('2018-02-28 01:43:44.447876', 3, 2, '2500000.00', '5000000.00', 2, 1),
('2018-02-28 01:43:44.447876', 4, 1, '2900000.00', '2900000.00', 7, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_followers`
--

CREATE TABLE `xlstore_followers` (
  `id` int(11) NOT NULL,
  `follow_date` datetime(6) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_companyadministrator`
--

CREATE TABLE `xlstore_managment_ms_companyadministrator` (
  `registration_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `email` varchar(200) NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(20) NOT NULL,
  `company_logo` varchar(100) DEFAULT NULL,
  `company_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_companyadministrator`
--

INSERT INTO `xlstore_managment_ms_companyadministrator` (`registration_date`, `id`, `email`, `username`, `password`, `company_logo`, `company_id`) VALUES
('2017-08-06 11:15:47.064000', 1, 'irchristianscott@gmail.com', 'admin', 'chriscott', '', 1),
('2017-09-14 12:25:48.152000', 2, 'hosanatextile@gmail.com', 'admin', 'ones', '', 2);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_companymobile`
--

CREATE TABLE `xlstore_managment_ms_companymobile` (
  `id` int(11) NOT NULL,
  `number` varchar(20) NOT NULL,
  `company_id` int(11) NOT NULL,
  `airline` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_companymobile`
--

INSERT INTO `xlstore_managment_ms_companymobile` (`id`, `number`, `company_id`, `airline`) VALUES
(1, '+256756891594', 1, 'Airtel');

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_companyteller`
--

CREATE TABLE `xlstore_managment_ms_companyteller` (
  `registration_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone_number` varchar(100) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `company_id` int(11) NOT NULL,
  `password` varchar(100) NOT NULL,
  `teller_image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_companyteller`
--

INSERT INTO `xlstore_managment_ms_companyteller` (`registration_date`, `id`, `full_name`, `username`, `email`, `address`, `phone_number`, `is_admin`, `company_id`, `password`, `teller_image`) VALUES
('2018-01-22 06:27:42.238772', 1, 'Abigael Bisimwa', 'abi', 'abibisimwa98@gmail.com', 'Goma, DRC', '+243978726536', 0, 1, '35771751', 'tellers/1516602462_26_IMG_1020.JPG');

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_licencekey`
--

CREATE TABLE `xlstore_managment_ms_licencekey` (
  `activated_date` date NOT NULL,
  `expary_date` date NOT NULL,
  `id` int(11) NOT NULL,
  `licence_key` varchar(255) NOT NULL,
  `status` varchar(120) NOT NULL,
  `company_id` int(11) NOT NULL,
  `ammount` int(11) NOT NULL,
  `currency` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_licencekey`
--

INSERT INTO `xlstore_managment_ms_licencekey` (`activated_date`, `expary_date`, `id`, `licence_key`, `status`, `company_id`, `ammount`, `currency`) VALUES
('2017-08-06', '2017-12-31', 1, 'd422881d-83fd-4a8e-b7f9-e972e9f27257', 'activated', 1, 100, 'USD'),
('2017-09-14', '2017-12-31', 2, '434747c6-7e4b-485c-b411-86821ee4265e', 'activated', 2, 100, 'USD');

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_licencekeyactivations`
--

CREATE TABLE `xlstore_managment_ms_licencekeyactivations` (
  `activated_date` date NOT NULL,
  `expary_date` date NOT NULL,
  `id` int(11) NOT NULL,
  `ammount` int(11) NOT NULL,
  `currency` varchar(50) NOT NULL,
  `company_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_licencekeyactivations`
--

INSERT INTO `xlstore_managment_ms_licencekeyactivations` (`activated_date`, `expary_date`, `id`, `ammount`, `currency`, `company_id`) VALUES
('2017-10-28', '2017-12-31', 8, 100, 'USD', 2),
('2017-10-28', '2017-12-31', 9, 100, 'USD', 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_productentry`
--

CREATE TABLE `xlstore_managment_ms_productentry` (
  `entry_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `quantity_before` int(11) NOT NULL,
  `quantity_added` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `item_price` decimal(18,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_productentry`
--

INSERT INTO `xlstore_managment_ms_productentry` (`entry_date`, `id`, `quantity_before`, `quantity_added`, `product_id`, `item_price`) VALUES
('2017-08-06 11:20:33.876000', 1, 0, 21, 1, '1000000.00'),
('2017-08-06 11:23:55.373000', 2, 0, 12, 2, '2100000.00'),
('2017-08-11 06:27:28.618000', 3, 0, 13, 3, '700000.00'),
('2017-08-11 06:54:26.700000', 4, 0, 12, 4, '2000000.00'),
('2017-09-03 04:48:40.672000', 5, 1, 13, 2, '1900000.00'),
('2017-09-14 19:24:52.355000', 6, 0, 12, 5, '20.00'),
('2017-09-14 19:25:16.737000', 7, 0, 10, 6, '17.00'),
('2017-09-19 05:30:29.565000', 8, 3, 12, 3, '800000.00'),
('2017-09-19 05:40:56.520000', 9, 2, 12, 1, '1000000.00'),
('2017-09-19 05:49:29.999000', 10, 3, 10, 4, '2000000.00'),
('2017-10-07 05:21:48.614000', 11, 2, 20, 2, '1800000.00'),
('2017-10-07 05:24:06.419000', 12, 4, 15, 1, '900000.00'),
('2018-01-23 15:19:52.907592', 13, 1, 20, 1, '800000.00'),
('2018-01-23 15:19:52.907592', 14, 3, 20, 2, '1800000.00'),
('2018-01-23 15:19:52.907592', 15, 3, 15, 4, '2000000.00'),
('2018-01-23 15:19:52.907592', 16, 5, 25, 3, '500000.00'),
('2018-01-24 02:59:29.125537', 17, 0, 20, 7, '2500000.00');

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_receiptdetails`
--

CREATE TABLE `xlstore_managment_ms_receiptdetails` (
  `saved_date` date NOT NULL,
  `id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `is_discounted` tinyint(1) NOT NULL,
  `discount` decimal(18,2) NOT NULL,
  `product_id` int(11) NOT NULL,
  `receipt_id` int(11) NOT NULL,
  `item_price` decimal(18,2),
  `is_trade` tinyint(1) NOT NULL,
  `trade_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_receiptdetails`
--

INSERT INTO `xlstore_managment_ms_receiptdetails` (`saved_date`, `id`, `quantity`, `total`, `is_discounted`, `discount`, `product_id`, `receipt_id`, `item_price`, `is_trade`, `trade_id`) VALUES
('2017-08-06', 1, 1, 2500000, 0, '0.00', 2, 1, '2500000.00', 0, NULL),
('2017-08-06', 2, 1, 1300000, 0, '0.00', 1, 1, '1300000.00', 0, NULL),
('2017-08-06', 3, 1, 2500000, 0, '0.00', 2, 2, '2500000.00', 0, NULL),
('2017-08-06', 4, 2, 2600000, 0, '0.00', 1, 2, '1300000.00', 0, NULL),
('2017-08-07', 5, 1, 2500000, 0, '0.00', 2, 3, '2500000.00', 0, NULL),
('2017-08-07', 6, 1, 2500000, 0, '0.00', 2, 4, '2500000.00', 0, NULL),
('2017-08-07', 7, 1, 1300000, 0, '0.00', 1, 4, '1300000.00', 0, NULL),
('2017-08-07', 8, 1, 2500000, 0, '0.00', 2, 5, '2500000.00', 0, NULL),
('2017-08-07', 9, 1, 1300000, 0, '0.00', 1, 5, '1300000.00', 0, NULL),
('2017-08-08', 10, 1, 1200000, 0, '0.00', 1, 6, '1200000.00', 0, NULL),
('2017-08-10', 11, 2, 2400000, 0, '0.00', 1, 7, '1200000.00', 0, NULL),
('2017-08-10', 12, 1, 2500000, 0, '0.00', 2, 8, '2500000.00', 0, NULL),
('2017-08-10', 13, 1, 1200000, 0, '0.00', 1, 8, '1200000.00', 0, NULL),
('2017-08-11', 14, 2, 5000000, 0, '0.00', 2, 9, '2500000.00', 0, NULL),
('2017-08-11', 15, 1, 2500000, 0, '0.00', 2, 10, '2500000.00', 0, NULL),
('2017-08-11', 16, 1, 1200000, 0, '0.00', 1, 10, '1200000.00', 0, NULL),
('2017-08-11', 17, 1, 1000000, 0, '0.00', 3, 10, '1000000.00', 0, NULL),
('2017-08-11', 18, 2, 2000000, 0, '0.00', 3, 11, '1000000.00', 0, NULL),
('2017-08-11', 19, 1, 1000000, 0, '0.00', 3, 12, '1000000.00', 0, NULL),
('2017-08-11', 20, 2, 2400000, 0, '0.00', 1, 12, '1200000.00', 0, NULL),
('2017-08-11', 21, 1, 2500000, 0, '0.00', 2, 13, '2500000.00', 0, NULL),
('2017-08-11', 22, 1, 1000000, 0, '0.00', 3, 13, '1000000.00', 0, NULL),
('2017-08-18', 23, 2, 5600000, 0, '0.00', 4, 14, '2800000.00', 0, NULL),
('2017-08-18', 24, 1, 1200000, 0, '0.00', 1, 14, '1200000.00', 0, NULL),
('2017-08-25', 25, 1, 2800000, 0, '0.00', 4, 15, '2800000.00', 0, NULL),
('2017-08-25', 26, 1, 1100000, 0, '0.00', 3, 15, '1100000.00', 0, NULL),
('2017-08-25', 27, 1, 1200000, 0, '0.00', 1, 16, '1200000.00', 0, NULL),
('2017-08-25', 28, 1, 1100000, 0, '0.00', 3, 16, '1100000.00', 0, NULL),
('2017-08-27', 29, 1, 1200000, 0, '0.00', 1, 17, '1200000.00', 0, NULL),
('2017-08-27', 30, 2, 5600000, 0, '0.00', 4, 17, '2800000.00', 0, NULL),
('2017-08-28', 36, 1, 2500000, 0, '0.00', 2, 18, '2500000.00', 0, NULL),
('2017-08-28', 37, 1, 1100000, 0, '0.00', 3, 18, '1100000.00', 0, NULL),
('2017-09-03', 38, 1, 2500000, 0, '0.00', 2, 19, '2500000.00', 0, NULL),
('2017-09-03', 39, 1, 1100000, 0, '0.00', 3, 19, '1100000.00', 0, NULL),
('2017-09-06', 40, 1, 2500000, 0, '0.00', 2, 20, '2500000.00', 0, NULL),
('2017-09-06', 41, 6, 7200000, 0, '0.00', 1, 20, '1200000.00', 0, NULL),
('2017-09-06', 42, 1, 2800000, 0, '0.00', 4, 20, '2800000.00', 0, NULL),
('2017-09-07', 43, 1, 2500000, 0, '0.00', 2, 21, '2500000.00', 0, NULL),
('2017-09-07', 44, 1, 2800000, 0, '0.00', 4, 21, '2800000.00', 0, NULL),
('2017-09-10', 45, 1, 1200000, 0, '0.00', 1, 22, '1200000.00', 0, NULL),
('2017-09-10', 46, 1, 2800000, 0, '0.00', 4, 22, '2800000.00', 0, NULL),
('2017-09-14', 47, 1, 2800000, 0, '0.00', 4, 23, '2800000.00', 0, NULL),
('2017-09-14', 50, 2, 2200000, 0, '0.00', 1, 23, '1100000.00', 1, 1),
('2017-09-14', 51, 1, 2500000, 0, '0.00', 2, 24, '2500000.00', 0, NULL),
('2017-09-18', 52, 2, 5000000, 0, '0.00', 2, 25, '2500000.00', 0, NULL),
('2017-09-19', 53, 1, 1100000, 0, '0.00', 3, 26, '1100000.00', 0, NULL),
('2017-09-19', 54, 2, 2200000, 0, '0.00', 1, 27, '1100000.00', 1, 1),
('2017-09-30', 55, 1, 2500000, 0, '0.00', 2, 28, '2500000.00', 0, NULL),
('2017-09-30', 56, 1, 1200000, 0, '0.00', 1, 28, '1200000.00', 0, NULL),
('2017-09-30', 57, 1, 2800000, 0, '0.00', 4, 29, '2800000.00', 0, NULL),
('2017-09-30', 58, 1, 2500000, 0, '0.00', 2, 29, '2500000.00', 0, NULL),
('2017-10-01', 59, 1, 2800000, 0, '0.00', 4, 30, '2800000.00', 0, NULL),
('2017-10-01', 60, 2, 5000000, 0, '0.00', 2, 30, '2500000.00', 0, NULL),
('2017-10-05', 61, 1, 1200000, 0, '0.00', 1, 31, '1200000.00', 0, NULL),
('2017-10-06', 62, 1, 2500000, 0, '0.00', 2, 32, '2500000.00', 0, NULL),
('2017-10-06', 63, 1, 2800000, 0, '0.00', 4, 32, '2800000.00', 0, NULL),
('2017-10-06', 64, 2, 2200000, 0, '0.00', 3, 33, '1100000.00', 0, NULL),
('2017-10-07', 65, 1, 1200000, 0, '0.00', 1, 34, '1200000.00', 0, NULL),
('2017-10-07', 66, 1, 2500000, 0, '0.00', 2, 34, '2500000.00', 0, NULL),
('2017-10-08', 67, 1, 2500000, 0, '0.00', 2, 35, '2500000.00', 0, NULL),
('2017-10-08', 68, 1, 1200000, 0, '0.00', 1, 35, '1200000.00', 0, NULL),
('2017-10-08', 69, 2, 2400000, 0, '0.00', 1, 36, '1200000.00', 0, NULL),
('2017-10-09', 70, 1, 30, 0, '0.00', 6, 37, '30.00', 0, NULL),
('2017-10-09', 71, 1, 25, 0, '0.00', 5, 37, '25.00', 0, NULL),
('2017-10-09', 72, 2, 50, 0, '0.00', 5, 38, '25.00', 0, NULL),
('2017-10-10', 73, 2, 60, 0, '0.00', 6, 39, '30.00', 0, NULL),
('2017-10-11', 74, 1, 30, 0, '0.00', 6, 40, '30.00', 0, NULL),
('2017-10-22', 75, 1, 2800000, 0, '0.00', 4, 41, '2800000.00', 0, NULL),
('2017-10-22', 76, 2, 5000000, 0, '0.00', 2, 41, '2500000.00', 0, NULL),
('2017-10-27', 77, 1, 2500000, 0, '0.00', 2, 42, '2500000.00', 0, NULL),
('2017-10-27', 78, 1, 2800000, 0, '0.00', 4, 42, '2800000.00', 0, NULL),
('2017-10-27', 79, 1, 1200000, 0, '0.00', 1, 42, '1200000.00', 0, NULL),
('2017-10-27', 80, 2, 2200000, 0, '0.00', 1, 43, '1100000.00', 1, 1),
('2017-10-28', 81, 1, 1200000, 0, '0.00', 1, 44, '1200000.00', 0, NULL),
('2017-10-28', 82, 1, 2500000, 0, '0.00', 2, 44, '2500000.00', 0, NULL),
('2017-10-29', 83, 2, 5000000, 0, '0.00', 2, 45, '2500000.00', 0, NULL),
('2017-10-29', 84, 1, 1100000, 0, '0.00', 3, 45, '1100000.00', 0, NULL),
('2017-11-07', 85, 1, 1200000, 0, '0.00', 1, 46, '1200000.00', 0, NULL),
('2017-11-07', 86, 1, 2800000, 0, '0.00', 4, 46, '2800000.00', 0, NULL),
('2017-11-18', 87, 1, 2500000, 0, '0.00', 2, 47, '2500000.00', 0, NULL),
('2017-11-20', 88, 1, 1200000, 0, '0.00', 1, 48, '1200000.00', 0, NULL),
('2017-11-20', 89, 1, 2500000, 0, '0.00', 2, 48, '2500000.00', 0, NULL),
('2017-11-21', 90, 1, 1200000, 0, '0.00', 1, 49, '1200000.00', 0, NULL),
('2017-11-21', 91, 1, 1100000, 0, '0.00', 3, 49, '1100000.00', 0, NULL),
('2017-11-28', 92, 1, 2800000, 0, '0.00', 4, 50, '2800000.00', 0, NULL),
('2017-11-28', 93, 1, 2500000, 0, '0.00', 2, 50, '2500000.00', 0, NULL),
('2017-11-28', 94, 2, 2400000, 0, '0.00', 1, 51, '1200000.00', 0, NULL),
('2017-11-28', 96, 1, 2500000, 0, '0.00', 2, 51, '2500000.00', 0, NULL),
('2017-11-28', 97, 1, 1100000, 0, '0.00', 3, 52, '1100000.00', 0, NULL),
('2017-11-28', 98, 1, 2500000, 0, '0.00', 2, 53, '2500000.00', 0, NULL),
('2017-12-01', 99, 1, 2800000, 0, '0.00', 4, 54, '2800000.00', 0, NULL),
('2017-12-01', 100, 1, 1100000, 0, '0.00', 3, 54, '1100000.00', 0, NULL),
('2017-12-05', 101, 2, 5000000, 0, '0.00', 2, 55, '2500000.00', 0, NULL),
('2017-12-05', 102, 1, 1100000, 0, '0.00', 3, 55, '1100000.00', 0, NULL),
('2017-12-05', 104, 2, 2200000, 0, '0.00', 1, 56, '1100000.00', 1, 1),
('2017-12-06', 105, 1, 2500000, 0, '0.00', 2, 57, '2500000.00', 0, NULL),
('2017-12-06', 106, 1, 1200000, 0, '0.00', 1, 57, '1200000.00', 0, NULL),
('2017-12-18', 107, 2, 2200000, 0, '0.00', 1, 58, '1100000.00', 1, 1),
('2017-12-18', 108, 1, 2500000, 0, '0.00', 2, 58, '2500000.00', 0, NULL),
('2018-01-23', 109, 1, 2800000, 0, '0.00', 4, 59, '2800000.00', 0, NULL),
('2018-01-23', 110, 1, 1100000, 0, '0.00', 3, 59, '1100000.00', 0, NULL),
('2018-01-23', 111, 1, 2500000, 0, '0.00', 2, 60, '2500000.00', 0, NULL),
('2018-01-23', 112, 1, 1100000, 0, '0.00', 3, 60, '1100000.00', 0, NULL),
('2018-01-23', 113, 1, 1200000, 0, '0.00', 1, 61, '1200000.00', 0, NULL),
('2018-01-23', 114, 1, 2800000, 0, '0.00', 4, 61, '2800000.00', 0, NULL),
('2018-01-23', 115, 1, 2500000, 0, '0.00', 2, 61, '2500000.00', 0, NULL),
('2018-01-23', 116, 1, 2500000, 0, '0.00', 2, 62, '2500000.00', 0, NULL),
('2018-01-23', 117, 1, 1100000, 0, '0.00', 3, 62, '1100000.00', 0, NULL),
('2018-01-23', 118, 1, 1200000, 0, '0.00', 1, 63, '1200000.00', 0, NULL),
('2018-01-23', 119, 1, 2500000, 0, '0.00', 2, 63, '2500000.00', 0, NULL),
('2018-01-24', 120, 1, 1200000, 0, '0.00', 1, 64, '1200000.00', 0, NULL),
('2018-01-25', 121, 1, 2900000, 0, '0.00', 7, 65, '2900000.00', 0, NULL),
('2018-01-25', 122, 1, 1200000, 0, '0.00', 1, 65, '1200000.00', 0, NULL),
('2018-01-25', 124, 1, 2500000, 0, '0.00', 2, 65, '2500000.00', 0, NULL),
('2018-01-25', 125, 1, 2900000, 0, '0.00', 7, 66, '2900000.00', 0, NULL),
('2018-01-25', 126, 1, 2900000, 0, '0.00', 7, 67, '2900000.00', 0, NULL),
('2018-01-25', 127, 1, 2500000, 0, '0.00', 2, 67, '2500000.00', 0, NULL),
('2018-01-25', 130, 1, 2800000, 0, '0.00', 4, 67, '2800000.00', 0, NULL),
('2018-01-25', 131, 1, 1100000, 0, '0.00', 3, 67, '1100000.00', 0, NULL),
('2018-01-25', 132, 1, 2900000, 0, '0.00', 7, 68, '2900000.00', 0, NULL),
('2018-01-25', 133, 1, 2500000, 0, '0.00', 2, 68, '2500000.00', 0, NULL),
('2018-01-26', 134, 1, 2500000, 0, '0.00', 2, 69, '2500000.00', 0, NULL),
('2018-01-26', 135, 1, 2900000, 0, '0.00', 7, 69, '2900000.00', 0, NULL),
('2018-01-26', 136, 1, 1100000, 0, '0.00', 3, 70, '1100000.00', 0, NULL),
('2018-01-26', 137, 1, 2500000, 0, '0.00', 2, 70, '2500000.00', 0, NULL),
('2018-02-11', 138, 1, 2900000, 0, '0.00', 7, 71, '2900000.00', 0, NULL),
('2018-02-11', 139, 1, 2500000, 0, '0.00', 2, 71, '2500000.00', 0, NULL),
('2018-02-26', 140, 1, 2500000, 0, '0.00', 2, 72, '2500000.00', 0, NULL),
('2018-02-28', 141, 1, 2900000, 0, '0.00', 7, 73, '2900000.00', 0, NULL),
('2018-02-28', 142, 1, 2800000, 0, '0.00', 4, 73, '2800000.00', 0, NULL),
('2018-03-05', 143, 1, 2900000, 0, '0.00', 7, 74, '2900000.00', 0, NULL),
('2018-03-05', 144, 1, 2500000, 0, '0.00', 2, 74, '2500000.00', 0, NULL),
('2018-03-05', 145, 1, 2500000, 0, '0.00', 2, 75, '2500000.00', 0, NULL),
('2018-03-05', 146, 1, 1200000, 0, '0.00', 1, 75, '1200000.00', 0, NULL),
('2018-03-05', 147, 1, 2800000, 0, '0.00', 4, 76, '2800000.00', 0, NULL),
('2018-03-05', 148, 1, 1200000, 0, '0.00', 1, 76, '1200000.00', 0, NULL),
('2018-03-05', 149, 1, 2500000, 0, '0.00', 2, 77, '2500000.00', 0, NULL),
('2018-03-05', 150, 1, 2900000, 0, '0.00', 7, 78, '2900000.00', 0, NULL),
('2018-03-05', 151, 1, 1100000, 0, '0.00', 3, 78, '1100000.00', 0, NULL),
('2018-03-05', 152, 1, 2900000, 0, '0.00', 7, 79, '2900000.00', 0, NULL),
('2018-03-05', 153, 1, 1200000, 0, '0.00', 1, 80, '1200000.00', 0, NULL),
('2018-03-05', 154, 2, 2200000, 0, '0.00', 3, 80, '1100000.00', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_receipts`
--

CREATE TABLE `xlstore_managment_ms_receipts` (
  `saved_date_timezone` datetime(6) NOT NULL,
  `saved_date` date NOT NULL,
  `id` int(11) NOT NULL,
  `receipt_number` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `other_charges` decimal(18,2) NOT NULL,
  `discount` decimal(18,2) NOT NULL,
  `total_paid` decimal(18,2) NOT NULL,
  `total_net` decimal(18,2) NOT NULL,
  `paid_by` varchar(100) NOT NULL,
  `company_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `teller_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_receipts`
--

INSERT INTO `xlstore_managment_ms_receipts` (`saved_date_timezone`, `saved_date`, `id`, `receipt_number`, `username`, `email`, `status`, `other_charges`, `discount`, `total_paid`, `total_net`, `paid_by`, `company_id`, `user_id`, `teller_id`) VALUES
('2017-08-06 14:04:07.312000', '2017-08-06', 1, 1, 'Christian Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '3800000.00', '3800000.00', 'cash', 1, NULL, NULL),
('2017-08-06 14:14:17.163000', '2017-08-06', 2, 2, 'Nelson Josue', 'irchristianscott@gmail.com', 'success', '0.00', '51000.00', '5100000.00', '5049000.00', 'cash', 1, NULL, NULL),
('2017-08-07 06:22:43.497000', '2017-08-07', 3, 3, '', NULL, 'success', '0.00', '0.00', '2500000.00', '2500000.00', 'cash', 1, 1, NULL),
('2017-08-07 09:19:33.732000', '2017-08-07', 4, 4, 'Kebron', '', 'success', '0.00', '15200.00', '3800000.00', '3784800.00', 'mobile', 1, NULL, NULL),
('2017-08-07 12:39:55.097000', '2017-08-07', 5, 5, 'Christian', '', 'success', '0.00', '0.00', '3800000.00', '3800000.00', 'cash', 1, NULL, NULL),
('2017-08-08 14:14:45.321000', '2017-08-08', 6, 6, '', NULL, 'success', '0.00', '0.00', '1200000.00', '1200000.00', 'cash', 1, 1, NULL),
('2017-08-09 21:31:33.470000', '2017-08-10', 7, 7, 'Alisa Princesse', '', 'success', '0.00', '0.00', '2400000.00', '2400000.00', 'paypal', 1, NULL, NULL),
('2017-08-10 15:43:03.023000', '2017-08-10', 8, 8, 'Gloire Ahadi', '', 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, NULL, NULL),
('2017-08-11 06:17:42.405000', '2017-08-11', 9, 9, '', NULL, 'success', '0.00', '0.00', '5000000.00', '5000000.00', 'cash', 1, 1, NULL),
('2017-08-11 06:26:38.204000', '2017-08-11', 10, 10, 'dfdf', '', 'success', '0.00', '0.00', '4700000.00', '4700000.00', 'cash', 1, NULL, NULL),
('2017-08-11 06:39:33.748000', '2017-08-11', 11, 11, 'User xx', '', 'success', '0.00', '2000.00', '2000000.00', '1998000.00', 'cash', 1, NULL, NULL),
('2017-08-11 06:50:46.466000', '2017-08-11', 12, 12, '', NULL, 'success', '0.00', '23800.00', '3400000.00', '3376200.00', 'cash', 1, 1, NULL),
('2017-08-11 10:37:18.335000', '2017-08-11', 13, 13, '', NULL, 'success', '0.00', '0.00', '3500000.00', '3500000.00', 'cash', 1, 1, NULL),
('2017-08-18 08:31:35.750000', '2017-08-18', 14, 14, '', NULL, 'success', '0.00', '12000.00', '4000000.00', '3988000.00', 'cash', 1, 1, NULL),
('2017-08-25 13:33:46.010000', '2017-08-25', 15, 15, '', NULL, 'success', '0.00', '35100.00', '3900000.00', '3864900.00', 'cash', 1, 1, NULL),
('2017-08-25 13:37:50.253000', '2017-08-25', 16, 16, 'customer 5', '', 'success', '0.00', '0.00', '2300000.00', '2300000.00', 'cash', 1, NULL, NULL),
('2017-08-27 15:24:36.164000', '2017-08-27', 17, 17, 'Kolesa Lurhakwa', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '6800000.00', '6800000.00', 'cash', 1, NULL, NULL),
('2017-08-28 04:02:56.184000', '2017-08-28', 18, 18, 'Alisa Lurhakwa', '', 'success', '0.00', '0.00', '3600000.00', '3600000.00', 'cash', 1, NULL, NULL),
('2017-09-03 04:49:49.032000', '2017-09-03', 19, 19, 'Customer x', '', 'success', '0.00', '0.00', '3600000.00', '3600000.00', 'cash', 1, NULL, NULL),
('2017-09-06 04:23:24.667000', '2017-09-06', 20, 20, 'Mother', 'irchristianscott@gmail.com', 'success', '0.00', '19500.00', '6500000.00', '6480500.00', 'cash', 1, NULL, NULL),
('2017-09-07 03:24:01.271000', '2017-09-07', 21, 21, 'Alisa', '', 'success', '0.00', '0.00', '5300000.00', '5300000.00', 'cash', 1, NULL, NULL),
('2017-09-10 05:57:10.781000', '2017-09-10', 22, 22, 'Onesphore', '', 'success', '0.00', '0.00', '4000000.00', '4000000.00', 'cash', 1, NULL, NULL),
('2017-09-14 08:03:55.443000', '2017-09-14', 23, 23, '', NULL, 'success', '0.00', '0.00', '5000000.00', '5000000.00', 'cash', 1, 1, NULL),
('2017-09-14 19:16:47.184000', '2017-09-14', 24, 24, '', NULL, 'success', '0.00', '0.00', '2500000.00', '2500000.00', 'cash', 1, 2, NULL),
('2017-09-18 13:27:22.153000', '2017-09-18', 25, 25, '', NULL, 'success', '0.00', '10000.00', '5000000.00', '4990000.00', 'cash', 1, 2, NULL),
('2017-09-19 05:28:17.023000', '2017-09-19', 26, 26, '', NULL, 'success', '0.00', '0.00', '1100000.00', '1100000.00', 'cash', 1, 1, NULL),
('2017-09-19 05:43:23.595000', '2017-09-19', 27, 27, '', NULL, 'success', '0.00', '0.00', '2200000.00', '2200000.00', 'cash', 1, 1, NULL),
('2017-09-30 05:50:02.781000', '2017-09-30', 28, 28, '', NULL, 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, 2, NULL),
('2017-09-30 05:53:44.648000', '2017-09-30', 29, 29, 'Onesphore', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '5300000.00', '5300000.00', 'cash', 1, NULL, NULL),
('2017-10-01 05:03:10.054000', '2017-10-01', 30, 30, '', NULL, 'success', '0.00', '78000.00', '7800000.00', '7722000.00', 'cash', 1, 2, NULL),
('2017-10-05 10:55:19.043000', '2017-10-05', 31, 31, 'David Koko', '', 'success', '0.00', '0.00', '1200000.00', '1200000.00', 'cash', 1, NULL, NULL),
('2017-10-06 05:09:07.047000', '2017-10-06', 32, 32, 'Nelson Josue', '', 'success', '0.00', '26500.00', '5300000.00', '5273500.00', 'cash', 1, NULL, NULL),
('2017-10-06 16:58:06.301000', '2017-10-06', 33, 33, '', NULL, 'success', '0.00', '0.00', '2200000.00', '2200000.00', 'cash', 1, 2, NULL),
('2017-10-07 05:20:40.479000', '2017-10-07', 34, 34, 'Germain B.', '', 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, NULL, NULL),
('2017-10-08 14:07:23.614000', '2017-10-08', 35, 35, 'David Koko M.', '', 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, NULL, NULL),
('2017-10-08 14:07:55.016000', '2017-10-08', 36, 36, '', NULL, 'success', '0.00', '0.00', '2400000.00', '2400000.00', 'cash', 1, 2, NULL),
('2017-10-09 17:01:17.075000', '2017-10-09', 37, 1, '', NULL, 'success', '0.00', '0.00', '55.00', '55.00', 'cash', 2, 2, NULL),
('2017-10-09 17:05:05.720000', '2017-10-09', 38, 2, 'M. Charite', '', 'success', '0.00', '0.00', '50.00', '50.00', 'cash', 2, NULL, NULL),
('2017-10-10 08:07:04.274000', '2017-10-10', 39, 3, 'M. Ajabu', '', 'success', '0.00', '0.00', '60.00', '59.00', 'cash', 2, NULL, NULL),
('2017-10-11 12:28:00.526000', '2017-10-11', 40, 4, '', NULL, 'success', '0.00', '0.00', '30.00', '30.00', 'cash', 2, 2, NULL),
('2017-10-22 04:55:48.691000', '2017-10-22', 41, 37, 'Ir Scott', '', 'success', '0.00', '0.00', '7800000.00', '7800000.00', 'cash', 1, NULL, NULL),
('2017-10-27 08:35:10.115000', '2017-10-27', 42, 38, '', NULL, 'success', '0.00', '0.00', '6500000.00', '6500000.00', 'cash', 1, 1, NULL),
('2017-10-27 08:35:45.617000', '2017-10-27', 43, 39, '', NULL, 'success', '0.00', '0.00', '2200000.00', '2200000.00', 'cash', 1, 1, NULL),
('2017-10-28 03:35:24.997000', '2017-10-28', 44, 40, '', NULL, 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, 2, NULL),
('2017-10-29 04:38:05.496000', '2017-10-29', 45, 41, 'Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '6100000.00', '6100000.00', 'cash', 1, NULL, NULL),
('2017-11-07 20:02:06.203000', '2017-11-07', 46, 42, 'Kolesa Lurhakwa', '', 'success', '0.00', '0.00', '4000000.00', '4000000.00', 'cash', 1, NULL, NULL),
('2017-11-18 04:33:20.380000', '2017-11-18', 47, 43, '', NULL, 'success', '0.00', '0.00', '2500000.00', '2500000.00', 'cash', 1, 2, NULL),
('2017-11-20 04:44:33.308000', '2017-11-20', 48, 44, 'David K.', '', 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, NULL, NULL),
('2017-11-21 03:17:35.919000', '2017-11-21', 49, 45, 'Onesphore', '', 'success', '0.00', '0.00', '2300000.00', '2300000.00', 'cash', 1, NULL, NULL),
('2017-11-28 03:50:52.492000', '2017-11-28', 50, 46, 'BAHATI Charlotte', '', 'success', '0.00', '0.00', '5300000.00', '5300000.00', 'cash', 1, NULL, NULL),
('2017-11-28 14:13:41.081000', '2017-11-28', 51, 47, '', NULL, 'success', '0.00', '0.00', '4900000.00', '4900000.00', 'cash', 1, 2, NULL),
('2017-11-28 14:50:51.313000', '2017-11-28', 52, 48, '', NULL, 'success', '0.00', '0.00', '1100000.00', '1100000.00', 'cash', 1, 1, NULL),
('2017-11-28 14:55:59.662000', '2017-11-28', 53, 49, 'User_2', '', 'success', '0.00', '12500.00', '2500000.00', '2487500.00', 'cash', 1, NULL, NULL),
('2017-12-01 19:03:04.238000', '2017-12-01', 54, 50, '', NULL, 'success', '0.00', '0.00', '3900000.00', '3900000.00', 'cash', 1, 2, NULL),
('2017-12-05 12:46:29.472000', '2017-12-05', 55, 51, 'Baraka Dubois', '', 'success', '0.00', '18300.00', '6100000.00', '6081700.00', 'cash', 1, NULL, NULL),
('2017-12-05 12:56:20.456000', '2017-12-05', 56, 52, '', NULL, 'success', '0.00', '0.00', '2200000.00', '2200000.00', 'cash', 1, 1, NULL),
('2017-12-06 13:15:50.735000', '2017-12-06', 57, 53, 'Carter', '', 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, NULL, NULL),
('2017-12-18 06:13:42.461000', '2017-12-18', 58, 54, '', NULL, 'success', '0.00', '0.00', '4700000.00', '4700000.00', 'cash', 1, 1, NULL),
('2018-01-23 07:11:02.578231', '2018-01-23', 59, 55, 'Christian Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '3900000.00', '3900000.00', 'cash', 1, NULL, 1),
('2018-01-23 13:35:35.922783', '2018-01-23', 60, 56, 'Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '3600000.00', '3600000.00', 'cash', 1, NULL, 1),
('2018-01-23 13:35:35.922783', '2018-01-23', 61, 57, 'Alisa', 'irchristianscott@gmail.com', 'success', '0.00', '19500.00', '6500000.00', '6480500.00', 'cash', 1, NULL, 1),
('2018-01-23 15:12:19.391322', '2018-01-23', 62, 58, 'Nelson Josue', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '3600000.00', '3600000.00', 'cash', 1, NULL, 1),
('2018-01-23 16:55:31.407537', '2018-01-23', 63, 59, 'Baraka Dubois', '', 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, NULL, 1),
('2018-01-24 01:54:36.657767', '2018-01-24', 64, 60, 'Onesphore', '', 'success', '0.00', '0.00', '1200000.00', '1200000.00', 'cash', 1, NULL, 1),
('2018-01-25 07:11:42.908491', '2018-01-25', 65, 61, 'Baraka Dubois', '', 'success', '0.00', '0.00', '6600000.00', '6600000.00', 'cash', 1, NULL, 1),
('2018-01-25 17:13:17.210244', '2018-01-25', 66, 62, '', NULL, 'success', '0.00', '0.00', '2900000.00', '2900000.00', 'cash', 1, 2, 1),
('2018-01-25 18:08:22.826724', '2018-01-25', 67, 63, '', NULL, 'success', '0.00', '93000.00', '9300000.00', '9207000.00', 'cash', 1, 1, 1),
('2018-01-25 18:08:22.826724', '2018-01-25', 68, 64, 'Nelly', '', 'success', '0.00', '0.00', '5400000.00', '5400000.00', 'cash', 1, NULL, 1),
('2018-01-26 08:18:07.998894', '2018-01-26', 69, 65, 'Leader', '', 'success', '0.00', '0.00', '5400000.00', '5400000.00', 'cash', 1, NULL, 1),
('2018-01-26 08:51:07.372763', '2018-01-26', 70, 66, 'David', '', 'success', '0.00', '0.00', '3600000.00', '3600000.00', 'cash', 1, NULL, NULL),
('2018-02-10 17:31:02.795283', '2018-02-11', 71, 67, 'Alisa', '', 'success', '0.00', '0.00', '5400000.00', '5400000.00', 'cash', 1, NULL, NULL),
('2018-02-26 03:49:07.823227', '2018-02-26', 72, 68, '', NULL, 'success', '0.00', '0.00', '2500000.00', '2500000.00', 'cash', 1, 1, NULL),
('2018-02-28 16:14:37.820664', '2018-02-28', 73, 69, '', NULL, 'success', '0.00', '0.00', '5700000.00', '5700000.00', 'cash', 1, 2, NULL),
('2018-03-05 04:08:00.786157', '2018-03-05', 74, 70, 'Christian Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '5400000.00', '5400000.00', 'cash', 1, NULL, NULL),
('2018-03-05 04:27:49.434225', '2018-03-05', 75, 71, 'Christian Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '3700000.00', '3700000.00', 'cash', 1, NULL, NULL),
('2018-03-05 04:27:49.434225', '2018-03-05', 76, 72, 'Chris Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '4000000.00', '4000000.00', 'cash', 1, NULL, NULL),
('2018-03-05 04:27:49.434225', '2018-03-05', 77, 73, 'Baraka Dubois', 'ms.xlstore@gmail.com', 'success', '0.00', '0.00', '2500000.00', '2500000.00', 'cash', 1, NULL, NULL),
('2018-03-05 05:02:27.333748', '2018-03-05', 78, 74, 'Alisa Princesse', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '4000000.00', '4000000.00', 'cash', 1, NULL, NULL),
('2018-03-05 05:04:37.136294', '2018-03-05', 79, 75, 'Germain Yannick', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '2900000.00', '2900000.00', 'cash', 1, NULL, NULL),
('2018-03-05 05:15:45.428353', '2018-03-05', 80, 76, 'Christian Scott', 'irchristianscott@gmail.com', 'success', '0.00', '0.00', '3400000.00', '3400000.00', 'cash', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_managment_ms_settings`
--

CREATE TABLE `xlstore_managment_ms_settings` (
  `id` int(11) NOT NULL,
  `reduce_after_trade_agreed` tinyint(1) NOT NULL,
  `allow_user_to_succeed` tinyint(1) NOT NULL,
  `print_bill` tinyint(1) NOT NULL,
  `currency` varchar(255) DEFAULT NULL,
  `internationalize` tinyint(1) NOT NULL,
  `access_market` tinyint(1) NOT NULL,
  `time_market_access` int(11) NOT NULL,
  `always_admin` tinyint(1) NOT NULL,
  `comment_product` tinyint(1) NOT NULL,
  `company_id` int(11) NOT NULL,
  `is_currency_changed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_managment_ms_settings`
--

INSERT INTO `xlstore_managment_ms_settings` (`id`, `reduce_after_trade_agreed`, `allow_user_to_succeed`, `print_bill`, `currency`, `internationalize`, `access_market`, `time_market_access`, `always_admin`, `comment_product`, `company_id`, `is_currency_changed`) VALUES
(1, 0, 0, 0, 'USH', 0, 0, 60, 0, 1, 1, 1),
(2, 0, 0, 0, 'USD', 0, 1, 30, 0, 1, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_ms_products`
--

CREATE TABLE `xlstore_ms_products` (
  `last_entry_stock` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `price` decimal(18,2) DEFAULT NULL,
  `stock` int(11) NOT NULL,
  `product_code` varchar(255) NOT NULL,
  `place_number` varchar(255) DEFAULT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_ms_products`
--

INSERT INTO `xlstore_ms_products` (`last_entry_stock`, `id`, `price`, `stock`, `product_code`, `place_number`, `product_id`) VALUES
('2018-01-23 15:19:52.907592', 1, '1300000.00', 15, '1273644', NULL, 3),
('2018-01-23 15:19:52.907592', 2, '2500000.00', 12, '2323445', NULL, 4),
('2018-01-23 15:19:52.907592', 3, '1000000.00', 25, '733656', NULL, 5),
('2018-01-23 15:19:52.907592', 4, '2800000.00', 15, '3443545', NULL, 2),
('2017-09-14 19:24:52.289000', 5, '25.00', 9, '6598324', NULL, 8),
('2017-09-14 19:25:16.663000', 6, '30.00', 6, '5645337', NULL, 9),
('2018-01-24 02:59:29.125537', 7, '2900000.00', 10, '16625142', NULL, 10);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_postmention`
--

CREATE TABLE `xlstore_postmention` (
  `mention_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `mention` longtext NOT NULL,
  `mentioner_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_postmention`
--

INSERT INTO `xlstore_postmention` (`mention_date`, `id`, `mention`, `mentioner_id`, `post_id`) VALUES
('2017-08-07 18:08:16.734000', 1, 'like', 1, 1),
('2017-08-08 12:37:08.584000', 2, 'like', 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_postreplies`
--

CREATE TABLE `xlstore_postreplies` (
  `reply_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `reply_type` longtext NOT NULL,
  `reply_image` varchar(100) DEFAULT NULL,
  `reply_text` longtext NOT NULL,
  `post_id` int(11) NOT NULL,
  `replyer_company_id` int(11) DEFAULT NULL,
  `replyer_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_postreplies`
--

INSERT INTO `xlstore_postreplies` (`reply_date`, `id`, `reply_type`, `reply_image`, `reply_text`, `post_id`, `replyer_company_id`, `replyer_user_id`) VALUES
('2017-08-07 17:22:17.852000', 1, 'company', '', 'no, we didint, or may be it wanst us', 2, 1, NULL),
('2017-08-07 17:26:02.005000', 2, 'user', '', 'im not really happy about this', 2, NULL, 1),
('2017-08-07 17:47:06.373000', 8, 'company', '', 'Hurry up', 1, 1, NULL),
('2017-08-11 06:25:59.406000', 9, 'company', '', 'youre wrong', 4, 1, NULL),
('2018-01-18 04:55:49.779242', 10, 'user', '', 'I will be right there', 10, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_posts`
--

CREATE TABLE `xlstore_posts` (
  `posted_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `poster_type` varchar(30) NOT NULL,
  `post_text` longtext NOT NULL,
  `post_file` varchar(100) DEFAULT NULL,
  `file_type` varchar(200) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  `poster_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_posts`
--

INSERT INTO `xlstore_posts` (`posted_date`, `id`, `poster_type`, `post_text`, `post_file`, `file_type`, `is_deleted`, `company_id`, `poster_id`) VALUES
('2017-08-07 02:29:06.582000', 1, 'company', 'Hey Guys..!! Something remarquable will be happening this saturday at @chriscotTech and 6:00 PM. Come and win one of our products. Thanks', '', '', 1, 1, NULL),
('2017-08-07 17:21:18.246000', 2, 'user', 'By the way, @chriscottTech gave me a fake mobile phone', '', '', 0, NULL, 1),
('2017-08-11 06:13:57.449000', 3, 'user', 'i baught from xxxxx http://127.0.0.1:8000/company/chriscottech.inc/products/item=3', '', '', 0, NULL, 1),
('2017-08-11 06:24:48.505000', 4, 'user', 'this is good sdgsd', '', '', 0, NULL, 1),
('2017-11-10 06:02:59.711000', 5, 'user', 'Hey Guys, I need this mobile phone. if you know the company that sells it, send me the link', 'posts/2017/11/10/Screenshot-2017-06-26-at-00.52.40.png', 'picture', 0, NULL, 1),
('2017-11-17 04:48:43.234000', 6, 'company', 'Hey Guys... ChroiscotTech want to launch a new product and it just wanted to invite all of you for this great event that will be held at Acacia Mall at 09:00 PM. Thanks', '', '', 0, 1, NULL),
('2017-12-06 15:47:17.584000', 7, 'company', 'Hey Guys...', '', '', 1, 1, NULL),
('2018-01-17 18:47:41.343281', 8, 'company', 'Hey Guys, Just informing you that our willer is Mr. @IrChriscott !!! Congratulations To Him', '', '', 1, 1, NULL),
('2018-01-18 04:54:54.422900', 10, 'company', 'Hey Guys, @IrChriscott is needed tomorrow in our offices', '', '', 1, 1, NULL),
('2018-01-18 16:19:20.508143', 11, 'company', 'Hello!!! Just to inform you that the winner of the <a href=\"/company/ChriscotTechInc/products/10/\" class=\"xl_mentioned_product\" data-product=\"10\">iPhone 7</a> is none else than <a href=\"/user/IrChriscott/\" class=\"xl_mentioned_user\" data-user=\"1\">@IrChriscott</a> !!! Congrats...', '', '', 0, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_productcomments`
--

CREATE TABLE `xlstore_productcomments` (
  `comment_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `commenter` varchar(200) NOT NULL,
  `comment` longtext NOT NULL,
  `commenter_company_id` int(11) DEFAULT NULL,
  `commenter_user_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_productcomments`
--

INSERT INTO `xlstore_productcomments` (`comment_date`, `id`, `commenter`, `comment`, `commenter_company_id`, `commenter_user_id`, `product_id`) VALUES
('2017-10-05 04:43:32.796000', 2, 'company', 'No, trust me, it is very cheap', 1, NULL, 4),
('2017-11-06 05:57:06.851000', 3, 'user', 'how much is it, i wanna get it', NULL, 1, 1),
('2018-02-09 13:55:04.911198', 4, 'company', 'djyufu', 1, NULL, 3);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_productinteress`
--

CREATE TABLE `xlstore_productinteress` (
  `interess_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `interesser_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_productinteress`
--

INSERT INTO `xlstore_productinteress` (`interess_date`, `id`, `interesser_id`, `product_id`) VALUES
('2017-08-23 04:38:17.285000', 1, 1, 4),
('2017-08-23 04:38:26.980000', 2, 1, 3),
('2017-08-25 13:28:07.942000', 3, 1, 6),
('2017-09-14 12:34:31.509000', 4, 2, 4),
('2017-11-10 19:03:49.446000', 5, 1, 8),
('2018-01-15 10:41:55.120103', 6, 2, 9),
('2018-01-15 10:42:09.289636', 7, 2, 8);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_productmention`
--

CREATE TABLE `xlstore_productmention` (
  `mention_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `mention` longtext NOT NULL,
  `mentioner_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_productmention`
--

INSERT INTO `xlstore_productmention` (`mention_date`, `id`, `mention`, `mentioner_id`, `product_id`) VALUES
('2018-03-01 04:24:42.951872', 1, 'dislike', 1, 5),
('2017-09-14 15:21:12.415000', 2, 'like', 2, 5),
('2018-03-01 04:24:17.587331', 5, 'like', 1, 10);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_productpictures`
--

CREATE TABLE `xlstore_productpictures` (
  `uploaded_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `product_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_productpictures`
--

INSERT INTO `xlstore_productpictures` (`uploaded_date`, `id`, `image`, `product_id`) VALUES
('2017-08-18 08:26:31.001000', 1, 'products/2017/08/18/1.jpg', 4),
('2017-08-18 08:26:31.145000', 2, 'products/2017/08/18/6.jpg', 4),
('2017-08-18 08:26:31.323000', 3, 'products/2017/08/18/8.jpg', 4);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_products`
--

CREATE TABLE `xlstore_products` (
  `posted_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `product_name` varchar(250) NOT NULL,
  `category` int(11) DEFAULT NULL,
  `image` varchar(100) NOT NULL,
  `price` decimal(18,2) NOT NULL,
  `currency` longtext NOT NULL,
  `product_description` longtext,
  `is_deleted` tinyint(1) NOT NULL,
  `is_to_be_posted` tinyint(1) NOT NULL,
  `company_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_products`
--

INSERT INTO `xlstore_products` (`posted_date`, `id`, `product_name`, `category`, `image`, `price`, `currency`, `product_description`, `is_deleted`, `is_to_be_posted`, `company_id`) VALUES
('2017-08-06 10:17:52.722000', 1, 'MacBook Air', 1, 'products/2017/08/06/mmac.jpg', '1800000.00', 'USH', '<p>Good Apple Laptop, with good properties:</p><ul><li>500GB HDD</li><li>4GB RAM</li><li>Intel core i5 2.3GHz CPU</li></ul>', 0, 1, 1),
('2017-08-06 10:56:25.885000', 2, 'iMac Retina 4K', 1, 'products/2017/08/06/4.jpg', '2800000.00', 'USH', '<p>New generation Apple desktop, with high properties</p><ul><li>Intel Core i5 2.8GHz CPU, Turbo Boost 3.7GHz</li><li>1TB HDD</li><li>16GB RAM</li><li>4k LDC Screen</li></ul>', 0, 0, 1),
('2017-08-06 11:14:33.683000', 3, 'iPhone 6', 2, 'products/2017/08/06/2.jpg', '1200000.00', 'USH', '<p>Second hand mobile phone from UK, 68GB of memory</p>', 0, 1, 1),
('2017-08-11 06:53:09.745000', 4, 'MacBook Pro', 1, 'products/2017/08/06/win.jpg', '2500000.00', 'USH', '<p>New Generation for Apple, MacBook Pro with high properties:</p><ul><li>1TB HDD</li><li>512GB SSD</li><li>16GB RAM</li><li>Intel Core i5 2.8GHz CPU</li><li>8hours battery life</li></ul>', 0, 1, 1),
('2017-08-18 08:35:11.372000', 5, 'iPhone 5S', 2, 'products/2017/08/11/1.png', '1100000.00', 'USH', '<p>Very strong mobile phone, second hand from UK, 64GB of memory</p>', 0, 1, 1),
('2017-08-25 13:27:24.907000', 6, 'iPhone 7+ (128GB)', 2, 'products/2017/08/25/4.jpg', '3200000.00', 'USH', '<p>Second hand iPhone 7 from UK with these details:</p><ul><li>second hand</li><li>128 gb</li><li>etc</li></ul>', 0, 1, 1),
('2017-09-14 12:24:12.817000', 7, 'Mousseline', 3, 'products/2017/09/14/tissus-habillement-tissu-mousseline-100-polyester-ros-4733123-mousse_47R7XTy.jpg', '23.00', 'USD', '<p>Tres belle tissu, lisse et de bonne qualite</p>', 0, 1, 2),
('2017-09-14 12:31:46.006000', 8, 'Tissue Satin', 3, 'products/2017/09/14/9184130199076.jpg', '25.00', 'USD', '<p>Tres belle qualite de tissu satin</p>', 0, 1, 2),
('2017-09-14 14:52:47.238000', 9, 'Tissue Tafta', 3, 'products/2017/09/14/109783_b_53027e23a2dd1f5d2effc99ae956c61b.jpg', '30.00', 'USD', '<p>Tres belle tissu pour rayonner votre habit et le faire angelique</p>', 0, 1, 2),
('2018-01-16 13:57:46.862834', 10, 'iPhone 7', 2, 'products/2018/01/16/apple-iphone-7-gallery-img-5.jpg', '2900000.00', 'USH', '<p>Brand new iPhone, 2nd hand.</p><ul><li>Gray Color</li><li>64GB of memory</li><li>Buy it and get a free cover and free Apple Stickers</li></ul>', 0, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_producttrade`
--

CREATE TABLE `xlstore_producttrade` (
  `started_date` datetime(6) NOT NULL,
  `end_date` datetime(6) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `status` varchar(50) NOT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_producttrade`
--

INSERT INTO `xlstore_producttrade` (`started_date`, `end_date`, `id`, `status`, `product_id`, `user_id`) VALUES
('2017-08-18 08:23:37.697000', '2017-10-04 16:35:57.461000', 1, 'succeeded', 4, 1),
('2018-01-29 15:16:16.290799', '2017-09-12 06:15:57.752000', 2, 'started', 3, 1),
('2017-09-03 13:45:50.877000', '2017-09-03 13:51:47.519000', 3, 'succeeded', 6, 1),
('2017-09-14 16:37:20.003000', NULL, 4, 'started', 4, 2);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_producttrademessages`
--

CREATE TABLE `xlstore_producttrademessages` (
  `date_time` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `sender` varchar(50) NOT NULL,
  `receiver` varchar(50) NOT NULL,
  `text_message` longtext,
  `image_message` varchar(100) DEFAULT NULL,
  `is_read` tinyint(1) NOT NULL,
  `is_deleted_by` varchar(40) NOT NULL,
  `trade_id` int(11) NOT NULL,
  `address` longtext,
  `latitude` varchar(18) DEFAULT NULL,
  `longitude` varchar(18) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_producttrademessages`
--

INSERT INTO `xlstore_producttrademessages` (`date_time`, `id`, `sender`, `receiver`, `text_message`, `image_message`, `is_read`, `is_deleted_by`, `trade_id`, `address`, `latitude`, `longitude`) VALUES
('2017-08-18 08:23:37.755000', 1, 'team', 'both', 'started', '', 0, 'none', 1, NULL, NULL, NULL),
('2017-08-18 08:23:51.684000', 2, 'user', 'company', 'gfg', '', 0, 'none', 1, NULL, NULL, NULL),
('2017-08-18 08:24:11.337000', 3, 'user', 'company', 'tfftf', '', 0, 'none', 1, NULL, NULL, NULL),
('2017-08-18 08:24:16.841000', 4, 'company', 'user', 'tftff', '', 0, 'none', 1, NULL, NULL, NULL),
('2017-08-21 05:04:19.639000', 5, 'user', 'company', 'how is the deal now??', '', 0, 'none', 1, NULL, NULL, NULL),
('2017-08-23 04:38:32.323000', 6, 'team', 'both', 'started', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-08-25 00:13:46.350000', 7, 'user', 'company', 'hey, i want to see images first', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-08-25 00:19:19.907000', 8, 'company', 'user', '', 'trades/2017/08/25/2.jpg', 0, 'none', 2, NULL, NULL, NULL),
('2017-08-25 00:19:20.067000', 9, 'company', 'user', '', 'trades/2017/08/25/4.jpg', 0, 'none', 2, NULL, NULL, NULL),
('2017-08-25 00:19:20.147000', 10, 'company', 'user', '', 'trades/2017/08/25/5.jpg', 0, 'none', 2, NULL, NULL, NULL),
('2017-08-25 04:36:37.853000', 11, 'user', 'company', 'Nice, I want to know your adress, send a map', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-09-03 13:45:50.979000', 17, 'team', 'both', 'started', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:48:30.121000', 18, 'team', 'both', 'started', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:48:34.113000', 19, 'company', 'user', 'hey', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:48:47.767000', 20, 'user', 'company', 'that was insaine', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:49:00.050000', 21, 'team', 'both', 'stopped', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:50:58.954000', 22, 'team', 'both', 'started', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:51:04.487000', 23, 'user', 'company', 'im sorry', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:51:25.300000', 24, 'user', 'company', 'i will give you 3.0 million', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:51:35.202000', 25, 'company', 'user', 'ok', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-03 13:51:47.604000', 26, 'team', 'both', 'succeeded', '', 0, 'none', 3, NULL, NULL, NULL),
('2017-09-12 05:10:40.841000', 27, 'company', 'user', '', '', 0, 'none', 2, 'Nana Hostels, Kathryn Free Way, Kampala, Uganda', '0.32487580', ' 32.56645100'),
('2017-09-12 06:14:55.806000', 28, 'user', 'company', 'im giving you 1m', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-09-12 06:15:15.082000', 29, 'company', 'user', 'No, 1.1m last', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-09-12 06:15:30.111000', 30, 'user', 'company', 'ok, you got yourself a deal', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-09-12 06:15:42.701000', 31, 'company', 'user', ':)', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-09-12 06:15:57.831000', 32, 'team', 'both', 'succeeded', '', 0, 'none', 2, NULL, NULL, NULL),
('2017-09-14 16:37:20.079000', 33, 'team', 'both', 'started', '', 0, 'none', 4, NULL, NULL, NULL),
('2017-10-04 16:35:57.538000', 34, 'team', 'both', 'succeeded', '', 0, 'none', 1, NULL, NULL, NULL),
('2018-01-12 07:55:10.450055', 36, 'user', 'company', 'hello', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-14 21:44:54.803050', 37, 'company', 'user', 'yes hello', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-14 21:45:38.594260', 38, 'user', 'company', 'yeah... I just wanted to know if i can get a loan from you', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-14 21:46:15.904023', 39, 'company', 'user', 'of what', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-14 22:26:19.765172', 40, 'user', 'company', 'of 3 macbook pro', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-14 22:26:28.450231', 41, 'company', 'user', 'ohh', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-14 22:26:46.882692', 42, 'company', 'user', 'hard to stipulate', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 05:51:21.727756', 43, 'user', 'company', 'how is that hard??', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 05:51:45.366337', 44, 'company', 'user', 'we are not a bank', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:16:24.254400', 45, 'team', 'both', 'stopped', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:18:16.018064', 46, 'team', 'both', 'started', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:18:50.563260', 47, 'user', 'company', 'sorry :(', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:30:11.698443', 48, 'team', 'both', 'stopped', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:39:18.059915', 49, 'team', 'both', 'started', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:40:02.041185', 50, 'company', 'user', 'That was my bad', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:40:30.567363', 51, 'user', 'company', 'yeah, you cann tell', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:42:42.932018', 52, 'user', 'company', 'what is next now', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:44:24.713264', 53, 'company', 'user', 'we will talk latter', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 06:45:54.824882', 54, 'user', 'company', 'okey :)', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-15 11:00:12.953733', 55, 'company', 'user', 'i am back', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-16 15:42:36.219616', 56, 'user', 'company', 'now, what are we gonna do', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-16 15:50:04.803326', 57, 'company', 'user', 'i have other things that can interess you', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-16 15:50:24.152407', 58, 'user', 'company', 'send pic please', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-16 15:52:26.039560', 59, 'company', 'user', '', 'trades/2018/01/16/macbook-air.jpg', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-16 15:52:26.104866', 60, 'company', 'user', '', 'trades/2018/01/16/MacBook-Pro-2016-12-1.png', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-16 15:52:26.138511', 61, 'company', 'user', '', 'trades/2018/01/16/mackbook-pro-buyers-guide-2.png', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-16 15:53:04.483318', 62, 'user', 'company', 'woww', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-17 06:25:06.248548', 63, 'team', 'both', 'stopped', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-17 07:06:31.444130', 64, 'team', 'both', 'started', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-17 14:22:30.861832', 65, 'team', 'both', 'stopped', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-17 14:47:21.732108', 66, 'team', 'both', 'started', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-18 14:15:14.323911', 67, 'user', 'company', 'send me your location', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-18 14:15:59.876735', 68, 'user', 'company', 'please', '', 0, 'none', 4, NULL, NULL, NULL),
('2018-01-18 14:18:26.527925', 69, 'company', 'user', '', '', 0, 'none', 4, 'Kampala, Aptech', '0.3105801', '32.58119439999996'),
('2018-01-29 15:16:16.406232', 70, 'team', 'both', 'started', '', 0, 'none', 2, NULL, NULL, NULL),
('2018-01-30 18:42:53.871357', 71, 'user', 'company', 'hello.. New deal??', '', 0, 'none', 2, NULL, NULL, NULL),
('2018-02-14 06:01:20.647208', 72, 'company', 'user', 'yeah but this time, meet me here', '', 0, 'none', 2, NULL, NULL, NULL),
('2018-02-14 06:01:59.720624', 73, 'company', 'user', '', '', 0, 'none', 2, 'Aptech Computer Education, Kampala, Uganda', '0.3105801', '32.58119439999996');

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_tradeagreements`
--

CREATE TABLE `xlstore_tradeagreements` (
  `agreement_date` date NOT NULL,
  `finished_date` date DEFAULT NULL,
  `id` int(11) NOT NULL,
  `price` decimal(18,2) NOT NULL,
  `quantity` int(11) NOT NULL,
  `status` varchar(100) NOT NULL,
  `is_finished` tinyint(1) NOT NULL,
  `trade_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_tradeagreements`
--

INSERT INTO `xlstore_tradeagreements` (`agreement_date`, `finished_date`, `id`, `price`, `quantity`, `status`, `is_finished`, `trade_id`) VALUES
('2017-12-18', '2017-12-25', 1, '2200000.00', 2, 'Finished', 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_user`
--

CREATE TABLE `xlstore_user` (
  `id` int(11) NOT NULL,
  `full_name` varchar(250) DEFAULT NULL,
  `user_name` varchar(250) NOT NULL,
  `email` varchar(254) NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `cover_image` varchar(100) DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `country` varchar(2) DEFAULT NULL,
  `town` longtext,
  `phone_number` longtext,
  `password` varchar(100) DEFAULT NULL,
  `biography` longtext,
  `show_secret_details` tinyint(1) NOT NULL,
  `is_authenticated` tinyint(1) NOT NULL,
  `registration_date` datetime(6) NOT NULL,
  `has_seen_tutorial` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_user`
--

INSERT INTO `xlstore_user` (`id`, `full_name`, `user_name`, `email`, `profile_image`, `cover_image`, `gender`, `country`, `town`, `phone_number`, `password`, `biography`, `show_secret_details`, `is_authenticated`, `registration_date`, `has_seen_tutorial`) VALUES
(1, 'Christian Lurhakwa', 'IrChriscott', 'christianlurhakwa@yahoo.fr', 'user_profile/1502086994_59_aaa.jpg', '', 'Male', 'UG', 'Kampala', '+256756891594', '12345', '', 1, 0, '2017-08-07 06:12:05.474000', 0),
(2, 'Alisa Lurhakwa', 'Princesse', 'alisaprincesse@gmail.com', '', '', 'Female', 'CD', 'Goma', NULL, 'alice123', NULL, 1, 0, '2017-09-14 12:18:41.521000', 0);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_usercategories`
--

CREATE TABLE `xlstore_usercategories` (
  `follow_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_usercategories`
--

INSERT INTO `xlstore_usercategories` (`follow_date`, `id`, `category_id`, `user_id`) VALUES
('2018-01-29 03:11:13.780008', 2, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_userfollow`
--

CREATE TABLE `xlstore_userfollow` (
  `follow_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `follower_user_id` int(11) NOT NULL,
  `following_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_userfollow`
--

INSERT INTO `xlstore_userfollow` (`follow_date`, `id`, `follower_user_id`, `following_id`) VALUES
('2017-09-05 13:07:50.599000', 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xlstore_usernotifications`
--

CREATE TABLE `xlstore_usernotifications` (
  `posted_date` datetime(6) NOT NULL,
  `id` int(11) NOT NULL,
  `notification_maker` varchar(100) NOT NULL,
  `notification_id` int(11) NOT NULL,
  `about` varchar(200) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  `concern_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xlstore_usernotifications`
--

INSERT INTO `xlstore_usernotifications` (`posted_date`, `id`, `notification_maker`, `notification_id`, `about`, `is_read`, `company_id`, `concern_id`, `user_id`) VALUES
('2017-09-05 13:07:50.719000', 1, 'user', 1, 'follow', 0, NULL, 1, 1),
('2018-01-18 04:54:54.509264', 2, 'company', 10, 'user_tagged', 0, 1, 1, NULL),
('2018-01-18 16:19:20.590932', 3, 'company', 11, 'user_tagged', 0, 1, 1, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `xlstore_address`
--
ALTER TABLE `xlstore_address`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_address_company_id_8af387e2_fk_xlstore_company_id` (`company_id`),
  ADD KEY `xlstore_address_user_id_6348b406_fk_xlstore_user_id` (`user_id`);

--
-- Indexes for table `xlstore_advertisments`
--
ALTER TABLE `xlstore_advertisments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_advertisments_company_id_c944ccac_fk_xlstore_company_id` (`company_id`),
  ADD KEY `xlstore_advertisments_product_id_08198001_fk_xlstore_products_id` (`product_id`);

--
-- Indexes for table `xlstore_categories`
--
ALTER TABLE `xlstore_categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_categories_company_id_3ff8bc60_fk_xlstore_company_id` (`company_id`);

--
-- Indexes for table `xlstore_company`
--
ALTER TABLE `xlstore_company`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `name_dotted` (`name_dotted`),
  ADD KEY `xlstore_company_category_id_1c003d81_fk_xlstore_c` (`category_id`);

--
-- Indexes for table `xlstore_companycategories`
--
ALTER TABLE `xlstore_companycategories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `xlstore_companynotifications`
--
ALTER TABLE `xlstore_companynotifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_companynotif_concern_id_ab0ab9a3_fk_xlstore_c` (`concern_id`),
  ADD KEY `xlstore_companynotifications_user_id_35c462fe_fk_xlstore_user_id` (`user_id`);

--
-- Indexes for table `xlstore_ecommerce_ec_companysettings`
--
ALTER TABLE `xlstore_ecommerce_ec_companysettings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xlstore_ecommerce_ec_companysettings_company_id_2dea7140_uniq` (`company_id`);

--
-- Indexes for table `xlstore_ecommerce_ec_marketaccess`
--
ALTER TABLE `xlstore_ecommerce_ec_marketaccess`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key` (`key`),
  ADD KEY `xlstore_ecommerce_ms_company_id_08892a55_fk_xlstore_m` (`company_id`),
  ADD KEY `xlstore_ecommerce_ms_user_id_c753a387_fk_xlstore_u` (`user_id`);

--
-- Indexes for table `xlstore_ecommerce_ec_shoppingcart`
--
ALTER TABLE `xlstore_ecommerce_ec_shoppingcart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_ecommerce_ms_market_id_8bcd94a2_fk_xlstore_e` (`market_id`);

--
-- Indexes for table `xlstore_ecommerce_ec_shoppingcartitems`
--
ALTER TABLE `xlstore_ecommerce_ec_shoppingcartitems`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_ecommerce_ms_product_id_54086c3a_fk_xlstore_m` (`product_id`),
  ADD KEY `xlstore_ecommerce_ec_cart_id_0ebeb519_fk_xlstore_e` (`cart_id`);

--
-- Indexes for table `xlstore_followers`
--
ALTER TABLE `xlstore_followers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_followers_company_id_d1f81fa6_fk_xlstore_company_id` (`company_id`),
  ADD KEY `xlstore_followers_user_id_ff2b69cd_fk_xlstore_user_id` (`user_id`);

--
-- Indexes for table `xlstore_managment_ms_companyadministrator`
--
ALTER TABLE `xlstore_managment_ms_companyadministrator`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `company_id` (`company_id`);

--
-- Indexes for table `xlstore_managment_ms_companymobile`
--
ALTER TABLE `xlstore_managment_ms_companymobile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_managment_ms_company_id_7669e914_fk_xlstore_m` (`company_id`);

--
-- Indexes for table `xlstore_managment_ms_companyteller`
--
ALTER TABLE `xlstore_managment_ms_companyteller`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_managment_ms_company_id_5eaeabc3_fk_xlstore_m` (`company_id`);

--
-- Indexes for table `xlstore_managment_ms_licencekey`
--
ALTER TABLE `xlstore_managment_ms_licencekey`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `licence_key` (`licence_key`),
  ADD UNIQUE KEY `company_id` (`company_id`);

--
-- Indexes for table `xlstore_managment_ms_licencekeyactivations`
--
ALTER TABLE `xlstore_managment_ms_licencekeyactivations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_managment_ms_company_id_43644450_fk_xlstore_m` (`company_id`);

--
-- Indexes for table `xlstore_managment_ms_productentry`
--
ALTER TABLE `xlstore_managment_ms_productentry`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_managment_ms_product_id_2f772509_fk_xlstore_m` (`product_id`);

--
-- Indexes for table `xlstore_managment_ms_receiptdetails`
--
ALTER TABLE `xlstore_managment_ms_receiptdetails`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_managment_ms_product_id_c4a32c33_fk_xlstore_m` (`product_id`),
  ADD KEY `xlstore_managment_ms_receipt_id_4ee073cf_fk_xlstore_m` (`receipt_id`),
  ADD KEY `xlstore_managment_ms_trade_id_d3069bf7_fk_xlstore_p` (`trade_id`);

--
-- Indexes for table `xlstore_managment_ms_receipts`
--
ALTER TABLE `xlstore_managment_ms_receipts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_managment_ms_company_id_642d9ce0_fk_xlstore_m` (`company_id`),
  ADD KEY `xlstore_managment_ms_user_id_552677da_fk_xlstore_u` (`user_id`),
  ADD KEY `xlstore_managment_ms_teller_id_e02fc011_fk_xlstore_m` (`teller_id`);

--
-- Indexes for table `xlstore_managment_ms_settings`
--
ALTER TABLE `xlstore_managment_ms_settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `company_id` (`company_id`);

--
-- Indexes for table `xlstore_ms_products`
--
ALTER TABLE `xlstore_ms_products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `xlstore_ms_products_product_id_2986bcfc_uniq` (`product_id`);

--
-- Indexes for table `xlstore_postmention`
--
ALTER TABLE `xlstore_postmention`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_postmention_mentioner_id_4293929b_fk_xlstore_user_id` (`mentioner_id`),
  ADD KEY `xlstore_postmention_post_id_c33a2e2c_fk_xlstore_posts_id` (`post_id`);

--
-- Indexes for table `xlstore_postreplies`
--
ALTER TABLE `xlstore_postreplies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_postreplies_post_id_1b91f005_fk_xlstore_posts_id` (`post_id`),
  ADD KEY `xlstore_postreplies_replyer_company_id_dbdd6d08_fk_xlstore_c` (`replyer_company_id`),
  ADD KEY `xlstore_postreplies_replyer_user_id_b44b627c_fk_xlstore_user_id` (`replyer_user_id`);

--
-- Indexes for table `xlstore_posts`
--
ALTER TABLE `xlstore_posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_posts_company_id_13e9e9d5_fk_xlstore_company_id` (`company_id`),
  ADD KEY `xlstore_posts_poster_id_f25308e9_fk_xlstore_user_id` (`poster_id`);

--
-- Indexes for table `xlstore_productcomments`
--
ALTER TABLE `xlstore_productcomments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_productcomme_commenter_company_id_96487dfe_fk_xlstore_c` (`commenter_company_id`),
  ADD KEY `xlstore_productcomme_commenter_user_id_b0ff6a89_fk_xlstore_u` (`commenter_user_id`),
  ADD KEY `xlstore_productcomme_product_id_ae6eea12_fk_xlstore_p` (`product_id`);

--
-- Indexes for table `xlstore_productinteress`
--
ALTER TABLE `xlstore_productinteress`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_productinter_interesser_id_18a5c989_fk_xlstore_u` (`interesser_id`),
  ADD KEY `xlstore_productinter_product_id_51e3f125_fk_xlstore_p` (`product_id`);

--
-- Indexes for table `xlstore_productmention`
--
ALTER TABLE `xlstore_productmention`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_productmention_mentioner_id_58d1314c_fk_xlstore_user_id` (`mentioner_id`),
  ADD KEY `xlstore_productmenti_product_id_acb880fd_fk_xlstore_p` (`product_id`);

--
-- Indexes for table `xlstore_productpictures`
--
ALTER TABLE `xlstore_productpictures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_productpictu_product_id_d543df1b_fk_xlstore_p` (`product_id`);

--
-- Indexes for table `xlstore_products`
--
ALTER TABLE `xlstore_products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_products_company_id_81415647_fk_xlstore_company_id` (`company_id`);

--
-- Indexes for table `xlstore_producttrade`
--
ALTER TABLE `xlstore_producttrade`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_producttrade_product_id_d5dbdd7b_fk_xlstore_products_id` (`product_id`),
  ADD KEY `xlstore_producttrade_user_id_14a05028_fk_xlstore_user_id` (`user_id`);

--
-- Indexes for table `xlstore_producttrademessages`
--
ALTER TABLE `xlstore_producttrademessages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_producttrade_trade_id_c76de0d0_fk_xlstore_p` (`trade_id`);

--
-- Indexes for table `xlstore_tradeagreements`
--
ALTER TABLE `xlstore_tradeagreements`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `trade_id` (`trade_id`);

--
-- Indexes for table `xlstore_user`
--
ALTER TABLE `xlstore_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_name` (`user_name`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `xlstore_usercategories`
--
ALTER TABLE `xlstore_usercategories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_usercategori_category_id_1a390dbf_fk_xlstore_c` (`category_id`),
  ADD KEY `xlstore_usercategories_user_id_412d9800_fk_xlstore_user_id` (`user_id`);

--
-- Indexes for table `xlstore_userfollow`
--
ALTER TABLE `xlstore_userfollow`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_userfollow_follower_user_id_077b9f79_fk_xlstore_user_id` (`follower_user_id`),
  ADD KEY `xlstore_userfollow_following_id_a939c453_fk_xlstore_user_id` (`following_id`);

--
-- Indexes for table `xlstore_usernotifications`
--
ALTER TABLE `xlstore_usernotifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `xlstore_usernotifica_company_id_d420fd2a_fk_xlstore_c` (`company_id`),
  ADD KEY `xlstore_usernotifications_concern_id_e1b7d431_fk_xlstore_user_id` (`concern_id`),
  ADD KEY `xlstore_usernotifications_user_id_5ecbb7a6_fk_xlstore_user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=157;
--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;
--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;
--
-- AUTO_INCREMENT for table `xlstore_address`
--
ALTER TABLE `xlstore_address`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_advertisments`
--
ALTER TABLE `xlstore_advertisments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_categories`
--
ALTER TABLE `xlstore_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `xlstore_company`
--
ALTER TABLE `xlstore_company`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `xlstore_companycategories`
--
ALTER TABLE `xlstore_companycategories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `xlstore_companynotifications`
--
ALTER TABLE `xlstore_companynotifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT for table `xlstore_ecommerce_ec_companysettings`
--
ALTER TABLE `xlstore_ecommerce_ec_companysettings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_ecommerce_ec_marketaccess`
--
ALTER TABLE `xlstore_ecommerce_ec_marketaccess`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_ecommerce_ec_shoppingcart`
--
ALTER TABLE `xlstore_ecommerce_ec_shoppingcart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `xlstore_ecommerce_ec_shoppingcartitems`
--
ALTER TABLE `xlstore_ecommerce_ec_shoppingcartitems`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `xlstore_followers`
--
ALTER TABLE `xlstore_followers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_companyadministrator`
--
ALTER TABLE `xlstore_managment_ms_companyadministrator`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_companymobile`
--
ALTER TABLE `xlstore_managment_ms_companymobile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_companyteller`
--
ALTER TABLE `xlstore_managment_ms_companyteller`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_licencekey`
--
ALTER TABLE `xlstore_managment_ms_licencekey`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_licencekeyactivations`
--
ALTER TABLE `xlstore_managment_ms_licencekeyactivations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_productentry`
--
ALTER TABLE `xlstore_managment_ms_productentry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_receiptdetails`
--
ALTER TABLE `xlstore_managment_ms_receiptdetails`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=155;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_receipts`
--
ALTER TABLE `xlstore_managment_ms_receipts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;
--
-- AUTO_INCREMENT for table `xlstore_managment_ms_settings`
--
ALTER TABLE `xlstore_managment_ms_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `xlstore_ms_products`
--
ALTER TABLE `xlstore_ms_products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `xlstore_postmention`
--
ALTER TABLE `xlstore_postmention`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `xlstore_postreplies`
--
ALTER TABLE `xlstore_postreplies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `xlstore_posts`
--
ALTER TABLE `xlstore_posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `xlstore_productcomments`
--
ALTER TABLE `xlstore_productcomments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `xlstore_productinteress`
--
ALTER TABLE `xlstore_productinteress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `xlstore_productmention`
--
ALTER TABLE `xlstore_productmention`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `xlstore_productpictures`
--
ALTER TABLE `xlstore_productpictures`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `xlstore_products`
--
ALTER TABLE `xlstore_products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `xlstore_producttrade`
--
ALTER TABLE `xlstore_producttrade`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `xlstore_producttrademessages`
--
ALTER TABLE `xlstore_producttrademessages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;
--
-- AUTO_INCREMENT for table `xlstore_tradeagreements`
--
ALTER TABLE `xlstore_tradeagreements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_user`
--
ALTER TABLE `xlstore_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `xlstore_usercategories`
--
ALTER TABLE `xlstore_usercategories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `xlstore_userfollow`
--
ALTER TABLE `xlstore_userfollow`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `xlstore_usernotifications`
--
ALTER TABLE `xlstore_usernotifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `xlstore_address`
--
ALTER TABLE `xlstore_address`
  ADD CONSTRAINT `xlstore_address_company_id_8af387e2_fk_xlstore_company_id` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_address_user_id_6348b406_fk_xlstore_user_id` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_advertisments`
--
ALTER TABLE `xlstore_advertisments`
  ADD CONSTRAINT `xlstore_advertisments_company_id_c944ccac_fk_xlstore_company_id` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_advertisments_product_id_08198001_fk_xlstore_products_id` FOREIGN KEY (`product_id`) REFERENCES `xlstore_products` (`id`);

--
-- Constraints for table `xlstore_categories`
--
ALTER TABLE `xlstore_categories`
  ADD CONSTRAINT `xlstore_categories_company_id_3ff8bc60_fk_xlstore_company_id` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`);

--
-- Constraints for table `xlstore_company`
--
ALTER TABLE `xlstore_company`
  ADD CONSTRAINT `xlstore_company_category_id_1c003d81_fk_xlstore_c` FOREIGN KEY (`category_id`) REFERENCES `xlstore_companycategories` (`id`);

--
-- Constraints for table `xlstore_companynotifications`
--
ALTER TABLE `xlstore_companynotifications`
  ADD CONSTRAINT `xlstore_companynotif_concern_id_ab0ab9a3_fk_xlstore_c` FOREIGN KEY (`concern_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_companynotifications_user_id_35c462fe_fk_xlstore_user_id` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_ecommerce_ec_companysettings`
--
ALTER TABLE `xlstore_ecommerce_ec_companysettings`
  ADD CONSTRAINT `xlstore_ecommerce_ec_company_id_2dea7140_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_companyadministrator` (`id`);

--
-- Constraints for table `xlstore_ecommerce_ec_marketaccess`
--
ALTER TABLE `xlstore_ecommerce_ec_marketaccess`
  ADD CONSTRAINT `xlstore_ecommerce_ms_company_id_08892a55_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_companyadministrator` (`id`),
  ADD CONSTRAINT `xlstore_ecommerce_ms_user_id_c753a387_fk_xlstore_u` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_ecommerce_ec_shoppingcart`
--
ALTER TABLE `xlstore_ecommerce_ec_shoppingcart`
  ADD CONSTRAINT `xlstore_ecommerce_ms_market_id_8bcd94a2_fk_xlstore_e` FOREIGN KEY (`market_id`) REFERENCES `xlstore_ecommerce_ec_marketaccess` (`id`);

--
-- Constraints for table `xlstore_ecommerce_ec_shoppingcartitems`
--
ALTER TABLE `xlstore_ecommerce_ec_shoppingcartitems`
  ADD CONSTRAINT `xlstore_ecommerce_ec_cart_id_0ebeb519_fk_xlstore_e` FOREIGN KEY (`cart_id`) REFERENCES `xlstore_ecommerce_ec_shoppingcart` (`id`),
  ADD CONSTRAINT `xlstore_ecommerce_ms_product_id_54086c3a_fk_xlstore_m` FOREIGN KEY (`product_id`) REFERENCES `xlstore_ms_products` (`id`);

--
-- Constraints for table `xlstore_followers`
--
ALTER TABLE `xlstore_followers`
  ADD CONSTRAINT `xlstore_followers_company_id_d1f81fa6_fk_xlstore_company_id` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_followers_user_id_ff2b69cd_fk_xlstore_user_id` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_managment_ms_companyadministrator`
--
ALTER TABLE `xlstore_managment_ms_companyadministrator`
  ADD CONSTRAINT `xlstore_managment_ms_company_id_74633eed_fk_xlstore_c` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`);

--
-- Constraints for table `xlstore_managment_ms_companymobile`
--
ALTER TABLE `xlstore_managment_ms_companymobile`
  ADD CONSTRAINT `xlstore_managment_ms_company_id_7669e914_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_companyadministrator` (`id`);

--
-- Constraints for table `xlstore_managment_ms_companyteller`
--
ALTER TABLE `xlstore_managment_ms_companyteller`
  ADD CONSTRAINT `xlstore_managment_ms_company_id_5eaeabc3_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_companyadministrator` (`id`);

--
-- Constraints for table `xlstore_managment_ms_licencekey`
--
ALTER TABLE `xlstore_managment_ms_licencekey`
  ADD CONSTRAINT `xlstore_managment_ms_company_id_c965f808_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_companyadministrator` (`id`);

--
-- Constraints for table `xlstore_managment_ms_licencekeyactivations`
--
ALTER TABLE `xlstore_managment_ms_licencekeyactivations`
  ADD CONSTRAINT `xlstore_managment_ms_company_id_43644450_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_licencekey` (`id`);

--
-- Constraints for table `xlstore_managment_ms_productentry`
--
ALTER TABLE `xlstore_managment_ms_productentry`
  ADD CONSTRAINT `xlstore_managment_ms_product_id_2f772509_fk_xlstore_m` FOREIGN KEY (`product_id`) REFERENCES `xlstore_ms_products` (`id`);

--
-- Constraints for table `xlstore_managment_ms_receiptdetails`
--
ALTER TABLE `xlstore_managment_ms_receiptdetails`
  ADD CONSTRAINT `xlstore_managment_ms_product_id_c4a32c33_fk_xlstore_m` FOREIGN KEY (`product_id`) REFERENCES `xlstore_ms_products` (`id`),
  ADD CONSTRAINT `xlstore_managment_ms_receipt_id_4ee073cf_fk_xlstore_m` FOREIGN KEY (`receipt_id`) REFERENCES `xlstore_managment_ms_receipts` (`id`),
  ADD CONSTRAINT `xlstore_managment_ms_trade_id_d3069bf7_fk_xlstore_p` FOREIGN KEY (`trade_id`) REFERENCES `xlstore_producttrade` (`id`);

--
-- Constraints for table `xlstore_managment_ms_receipts`
--
ALTER TABLE `xlstore_managment_ms_receipts`
  ADD CONSTRAINT `xlstore_managment_ms_company_id_642d9ce0_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_companyadministrator` (`id`),
  ADD CONSTRAINT `xlstore_managment_ms_teller_id_e02fc011_fk_xlstore_m` FOREIGN KEY (`teller_id`) REFERENCES `xlstore_managment_ms_companyteller` (`id`),
  ADD CONSTRAINT `xlstore_managment_ms_user_id_552677da_fk_xlstore_u` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_managment_ms_settings`
--
ALTER TABLE `xlstore_managment_ms_settings`
  ADD CONSTRAINT `xlstore_managment_ms_company_id_d5f499d3_fk_xlstore_m` FOREIGN KEY (`company_id`) REFERENCES `xlstore_managment_ms_companyadministrator` (`id`);

--
-- Constraints for table `xlstore_ms_products`
--
ALTER TABLE `xlstore_ms_products`
  ADD CONSTRAINT `xlstore_ms_products_product_id_2986bcfc_fk_xlstore_products_id` FOREIGN KEY (`product_id`) REFERENCES `xlstore_products` (`id`);

--
-- Constraints for table `xlstore_postmention`
--
ALTER TABLE `xlstore_postmention`
  ADD CONSTRAINT `xlstore_postmention_mentioner_id_4293929b_fk_xlstore_user_id` FOREIGN KEY (`mentioner_id`) REFERENCES `xlstore_user` (`id`),
  ADD CONSTRAINT `xlstore_postmention_post_id_c33a2e2c_fk_xlstore_posts_id` FOREIGN KEY (`post_id`) REFERENCES `xlstore_posts` (`id`);

--
-- Constraints for table `xlstore_postreplies`
--
ALTER TABLE `xlstore_postreplies`
  ADD CONSTRAINT `xlstore_postreplies_post_id_1b91f005_fk_xlstore_posts_id` FOREIGN KEY (`post_id`) REFERENCES `xlstore_posts` (`id`),
  ADD CONSTRAINT `xlstore_postreplies_replyer_company_id_dbdd6d08_fk_xlstore_c` FOREIGN KEY (`replyer_company_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_postreplies_replyer_user_id_b44b627c_fk_xlstore_user_id` FOREIGN KEY (`replyer_user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_posts`
--
ALTER TABLE `xlstore_posts`
  ADD CONSTRAINT `xlstore_posts_company_id_13e9e9d5_fk_xlstore_company_id` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_posts_poster_id_f25308e9_fk_xlstore_user_id` FOREIGN KEY (`poster_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_productcomments`
--
ALTER TABLE `xlstore_productcomments`
  ADD CONSTRAINT `xlstore_productcomme_commenter_company_id_96487dfe_fk_xlstore_c` FOREIGN KEY (`commenter_company_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_productcomme_commenter_user_id_b0ff6a89_fk_xlstore_u` FOREIGN KEY (`commenter_user_id`) REFERENCES `xlstore_user` (`id`),
  ADD CONSTRAINT `xlstore_productcomme_product_id_ae6eea12_fk_xlstore_p` FOREIGN KEY (`product_id`) REFERENCES `xlstore_products` (`id`);

--
-- Constraints for table `xlstore_productinteress`
--
ALTER TABLE `xlstore_productinteress`
  ADD CONSTRAINT `xlstore_productinter_interesser_id_18a5c989_fk_xlstore_u` FOREIGN KEY (`interesser_id`) REFERENCES `xlstore_user` (`id`),
  ADD CONSTRAINT `xlstore_productinter_product_id_51e3f125_fk_xlstore_p` FOREIGN KEY (`product_id`) REFERENCES `xlstore_products` (`id`);

--
-- Constraints for table `xlstore_productmention`
--
ALTER TABLE `xlstore_productmention`
  ADD CONSTRAINT `xlstore_productmenti_product_id_acb880fd_fk_xlstore_p` FOREIGN KEY (`product_id`) REFERENCES `xlstore_products` (`id`),
  ADD CONSTRAINT `xlstore_productmention_mentioner_id_58d1314c_fk_xlstore_user_id` FOREIGN KEY (`mentioner_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_productpictures`
--
ALTER TABLE `xlstore_productpictures`
  ADD CONSTRAINT `xlstore_productpictu_product_id_d543df1b_fk_xlstore_p` FOREIGN KEY (`product_id`) REFERENCES `xlstore_products` (`id`);

--
-- Constraints for table `xlstore_products`
--
ALTER TABLE `xlstore_products`
  ADD CONSTRAINT `xlstore_products_company_id_81415647_fk_xlstore_company_id` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`);

--
-- Constraints for table `xlstore_producttrade`
--
ALTER TABLE `xlstore_producttrade`
  ADD CONSTRAINT `xlstore_producttrade_product_id_d5dbdd7b_fk_xlstore_products_id` FOREIGN KEY (`product_id`) REFERENCES `xlstore_products` (`id`),
  ADD CONSTRAINT `xlstore_producttrade_user_id_14a05028_fk_xlstore_user_id` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_producttrademessages`
--
ALTER TABLE `xlstore_producttrademessages`
  ADD CONSTRAINT `xlstore_producttrade_trade_id_c76de0d0_fk_xlstore_p` FOREIGN KEY (`trade_id`) REFERENCES `xlstore_producttrade` (`id`);

--
-- Constraints for table `xlstore_tradeagreements`
--
ALTER TABLE `xlstore_tradeagreements`
  ADD CONSTRAINT `xlstore_tradeagreeme_trade_id_59ed0977_fk_xlstore_p` FOREIGN KEY (`trade_id`) REFERENCES `xlstore_producttrade` (`id`);

--
-- Constraints for table `xlstore_usercategories`
--
ALTER TABLE `xlstore_usercategories`
  ADD CONSTRAINT `xlstore_usercategori_category_id_1a390dbf_fk_xlstore_c` FOREIGN KEY (`category_id`) REFERENCES `xlstore_companycategories` (`id`),
  ADD CONSTRAINT `xlstore_usercategories_user_id_412d9800_fk_xlstore_user_id` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_userfollow`
--
ALTER TABLE `xlstore_userfollow`
  ADD CONSTRAINT `xlstore_userfollow_follower_user_id_077b9f79_fk_xlstore_user_id` FOREIGN KEY (`follower_user_id`) REFERENCES `xlstore_user` (`id`),
  ADD CONSTRAINT `xlstore_userfollow_following_id_a939c453_fk_xlstore_user_id` FOREIGN KEY (`following_id`) REFERENCES `xlstore_user` (`id`);

--
-- Constraints for table `xlstore_usernotifications`
--
ALTER TABLE `xlstore_usernotifications`
  ADD CONSTRAINT `xlstore_usernotifica_company_id_d420fd2a_fk_xlstore_c` FOREIGN KEY (`company_id`) REFERENCES `xlstore_company` (`id`),
  ADD CONSTRAINT `xlstore_usernotifications_concern_id_e1b7d431_fk_xlstore_user_id` FOREIGN KEY (`concern_id`) REFERENCES `xlstore_user` (`id`),
  ADD CONSTRAINT `xlstore_usernotifications_user_id_5ecbb7a6_fk_xlstore_user_id` FOREIGN KEY (`user_id`) REFERENCES `xlstore_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
