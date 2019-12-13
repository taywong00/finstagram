-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 13, 2019 at 02:39 AM
-- Server version: 5.7.26
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Finstagram`
--

-- --------------------------------------------------------

--
-- Table structure for table `Person`
--

CREATE TABLE `Person` (
  `username` varchar(20) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `firstName` varchar(20) DEFAULT NULL,
  `lastName` varchar(20) DEFAULT NULL,
  `bio` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Person`
--

INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`) VALUES
('abby', '843c26886370206f24a10c72352a9a1c1ffe0e0680a1ba2975022e74149b55b7', 'Abby', 'Lee', 'Dance Moms Leader'),
('andybaraghani', '94c1710e9385f59b68a9398aedc785d0d3c497fc097a0799f48e8ef741c907ba', 'Andy', 'Baraghani', 'Senior Food Editor, Bon Appetit and Healthyish'),
('bobby', 'a144afa2252d767676ac0e088f8fec78f0b397be76d5b7c86b7d3c7d8a6737eb', 'Bobby', 'Brown', 'Abbys Partner'),
('brad_leone', '7661ef3f13c973dd022857d8c83305a5f45051a4fd329d5585cb11a1e8772f46', 'Brad', 'Leone', 'Human being. Let\'s never stop learning.. love is the light.'),
('colieen', '394ba10309d56db40df87344f63ee92c21fbbb6438e97a8ae0d0f1c03a3aa7e4', 'Colieen', 'Douglas', 'Dance Mom'),
('csaffitz', '315ef8557f8df0f6e6cefff9e185ba238010c5fb113048e9cfbf7c7aa1104e23', 'Claire', 'Saffitz', 'Contributing writer at Bon Appetit/Star of Gourmet Makes'),
('dan', 'a144afa2252d767676ac0e088f8fec78f0b397be76d5b7c86b7d3c7d8a6737eb', 'Dan', 'Sucio', 'dirty dan'),
('jaap.deinum', 'a8e55bb7f6f6052ffb35a733dde602ff3d4054ea9f4f582afb9a4ad18e5c065f', 'Jaap', 'Deinum', 'NYU Tisch ‘22'),
('jerrygreenfield_', '248d043214e895e1d018c042bf7da6c172c0beb89438515f7aa84e7a82f2cf24', 'Jeremiah', 'Campoverde', 'Are you lost enough?'),
('lallimusic', 'a3217d362f3df478a46f138a44f3b60fcd1f806aa9de6f25821011c84c88d426', 'Carla', 'Lalli Music', 'Food Director'),
('mayafinky', '4ce2005b8d4dd41a8cc5221ac08e83551f332457e6c6864b36c7c0c42fdd53e8', 'Maya', 'Finkman', 'unemployed in greenland // nyu'),
('mollybaz', '93977bc1813b2320d2e15626f079109d0889053b41e64b4dc6e07e4b0ceeab7b', 'Molly', 'Baz', 'Senior Food Editor, Bon Appétit. Cartoon Character; Cae Sal Enthusiast'),
('moroccochris', '6849cdc8e45e9303d9fe5e0eacacfad718d3c13c9045544a1f3a046e6044ffc7', 'Chris', 'Morocco', 'Deputy Food Editor, Bon Appetit and Healthyish'),
('rapoport', '5a53040b807756a32ebb4891e42311f61b9d72e787f3ca17b3aae24ae85fe36f', 'Adam', 'Rapoport', 'Editor in chief of Bon Appétit'),
('TestUser', 'f981c9e062f68e5a10f8314497d1120d96438e7f6783f9487a975ef4e0c5d065', 'Jane', 'Doe', 'I love pie!');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Person`
--
ALTER TABLE `Person`
  ADD PRIMARY KEY (`username`);
