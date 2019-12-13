-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 13, 2019 at 03:15 AM
-- Server version: 5.7.26
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Finstagram`
--

-- --------------------------------------------------------

--
-- Table structure for table `BelongTo`
--

CREATE TABLE `BelongTo` (
  `member_username` varchar(20) NOT NULL,
  `owner_username` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `BelongTo`
--

INSERT INTO `BelongTo` (`member_username`, `owner_username`, `groupName`) VALUES
('abby', 'abby', 'family'),
('dan', 'abby', 'family'),
('abby', 'abby', 'roommates'),
('colieen', 'abby', 'roommates'),
('bobby', 'bobby', 'roommates'),
('dan', 'bobby', 'roommates'),
('andybaraghani', 'rapoport', 'testkitchen'),
('brad_leone', 'rapoport', 'testkitchen'),
('csaffitz', 'rapoport', 'testkitchen'),
('lallimusic', 'rapoport', 'testkitchen'),
('mollybaz', 'rapoport', 'testkitchen'),
('moroccochris', 'rapoport', 'testkitchen'),
('rapoport', 'rapoport', 'testkitchen'),
('TestUser', 'rapoport', 'testkitchen'),
('jaap.deinum', 'TestUser', 'oct3'),
('jerrygreenfield_', 'TestUser', 'oct3'),
('mayafinky', 'TestUser', 'oct3'),
('TestUser', 'TestUser', 'oct3');

-- --------------------------------------------------------

--
-- Table structure for table `Follow`
--

CREATE TABLE `Follow` (
  `username_followed` varchar(20) NOT NULL,
  `username_follower` varchar(20) NOT NULL,
  `followstatus` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Follow`
--

INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES
('abby', 'TestUser', 1),
('bobby', 'abby', 1),
('bobby', 'colieen', 0),
('bobby', 'TestUser', 1),
('TestUser', 'abby', 1),
('TestUser', 'andybaraghani', 1),
('TestUser', 'jaap.deinum', 0),
('TestUser', 'lallimusic', 1),
('TestUser', 'rapoport', 0);

-- --------------------------------------------------------

--
-- Table structure for table `Friendgroup`
--

CREATE TABLE `Friendgroup` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `description` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Friendgroup`
--

INSERT INTO `Friendgroup` (`groupOwner`, `groupName`, `description`) VALUES
('abby', 'family', 'Lee Family'),
('abby', 'roommates', 'roommates of 221B'),
('bobby', 'bowlingTeam', 'The Pinhead Larrys'),
('bobby', 'roommates', '42 Wallaby Way'),
('rapoport', 'testkitchen', 'The Bon Appetit Test Kitchen'),
('TestUser', 'oct3', 'Oct 3');

-- --------------------------------------------------------

--
-- Table structure for table `Likes`
--

CREATE TABLE `Likes` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `liketime` datetime DEFAULT NULL,
  `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Likes`
--

INSERT INTO `Likes` (`username`, `photoID`, `liketime`, `rating`) VALUES
('TestUser', 2, '2019-11-30 00:00:00', 4);

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

-- --------------------------------------------------------

--
-- Table structure for table `Photo`
--

CREATE TABLE `Photo` (
  `photoID` int(11) NOT NULL,
  `postingdate` datetime DEFAULT NULL,
  `filepath` varchar(100) DEFAULT NULL,
  `allFollowers` tinyint(1) DEFAULT NULL,
  `caption` varchar(100) DEFAULT NULL,
  `photoPoster` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Photo`
--

INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES
(1, '2019-11-29 00:00:00', '../static/photo_library/roommates_b.jpeg', 1, 'roommates', 'bobby'),
(2, '2019-11-30 00:00:00', '../static/photo_library/roommates_a.jpg', 1, 'roommates', 'abby'),
(3, '2019-11-30 00:00:00', '../static/photo_library/bowling_team.jpg', 0, 'bowlingTeam', 'bobby'),
(4, '2019-11-30 00:00:00', '../static/photo_library/family_bora_bora.jpg', 0, 'family vaca', 'abby'),
(5, '2019-12-07 10:04:29', '../static/photo_library/gbbo.jpg', 0, 'I love the Great British Bake Off', 'TestUser'),
(6, '2019-12-08 05:18:01', '../static/photo_library/batk-staff.jpg', 0, 'The Gang\'s All Here', 'TestUser'),
(7, '2019-12-11 23:00:27', '../static/photo_library/buble.jpg', 0, 'I love pie but I also love Christmas', 'TestUser');

-- --------------------------------------------------------

--
-- Table structure for table `SharedWith`
--

CREATE TABLE `SharedWith` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `SharedWith`
--

INSERT INTO `SharedWith` (`groupOwner`, `groupName`, `photoID`) VALUES
('bobby', 'roommates', 3),
('rapoport', 'testkitchen', 5),
('TestUser', 'oct3', 5),
('rapoport', 'testkitchen', 6),
('rapoport', 'testkitchen', 7),
('TestUser', 'oct3', 7);

-- --------------------------------------------------------

--
-- Table structure for table `Tagged`
--

CREATE TABLE `Tagged` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `tagstatus` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Tagged`
--

INSERT INTO `Tagged` (`username`, `photoID`, `tagstatus`) VALUES
('abby', 1, 0),
('TestUser', 1, 1),
('TestUser', 2, 1),
('TestUser', 6, 1),
('TestUser', 7, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `BelongTo`
--
ALTER TABLE `BelongTo`
  ADD PRIMARY KEY (`member_username`,`owner_username`,`groupName`),
  ADD KEY `owner_username` (`owner_username`,`groupName`);

--
-- Indexes for table `Follow`
--
ALTER TABLE `Follow`
  ADD PRIMARY KEY (`username_followed`,`username_follower`),
  ADD KEY `username_follower` (`username_follower`);

--
-- Indexes for table `Friendgroup`
--
ALTER TABLE `Friendgroup`
  ADD PRIMARY KEY (`groupOwner`,`groupName`);

--
-- Indexes for table `Likes`
--
ALTER TABLE `Likes`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- Indexes for table `Person`
--
ALTER TABLE `Person`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `Photo`
--
ALTER TABLE `Photo`
  ADD PRIMARY KEY (`photoID`),
  ADD KEY `photoPoster` (`photoPoster`);

--
-- Indexes for table `SharedWith`
--
ALTER TABLE `SharedWith`
  ADD PRIMARY KEY (`groupOwner`,`groupName`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- Indexes for table `Tagged`
--
ALTER TABLE `Tagged`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Photo`
--
ALTER TABLE `Photo`
  MODIFY `photoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `BelongTo`
--
ALTER TABLE `BelongTo`
  ADD CONSTRAINT `belongto_ibfk_1` FOREIGN KEY (`member_username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `belongto_ibfk_2` FOREIGN KEY (`owner_username`,`groupName`) REFERENCES `Friendgroup` (`groupOwner`, `groupName`);

--
-- Constraints for table `Follow`
--
ALTER TABLE `Follow`
  ADD CONSTRAINT `follow_ibfk_1` FOREIGN KEY (`username_followed`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `follow_ibfk_2` FOREIGN KEY (`username_follower`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Friendgroup`
--
ALTER TABLE `Friendgroup`
  ADD CONSTRAINT `friendgroup_ibfk_1` FOREIGN KEY (`groupOwner`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Likes`
--
ALTER TABLE `Likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Photo`
--
ALTER TABLE `Photo`
  ADD CONSTRAINT `photo_ibfk_1` FOREIGN KEY (`photoPoster`) REFERENCES `Person` (`username`);

--
-- Constraints for table `SharedWith`
--
ALTER TABLE `SharedWith`
  ADD CONSTRAINT `sharedwith_ibfk_1` FOREIGN KEY (`groupOwner`,`groupName`) REFERENCES `Friendgroup` (`groupOwner`, `groupName`),
  ADD CONSTRAINT `sharedwith_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Tagged`
--
ALTER TABLE `Tagged`
  ADD CONSTRAINT `tagged_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `tagged_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);
