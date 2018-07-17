import sqlite3

db = sqlite3.connect('test.db');
script = '''
-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'user'
-- 
-- ---

DROP TABLE IF EXISTS `user`;
        
CREATE TABLE `user` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `created` DATETIME NOT NULL,
  `name` VARCHAR NOT NULL
);

-- ---
-- Table 'post'
-- 
-- ---

DROP TABLE IF EXISTS `post`;
        
CREATE TABLE `post` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `created` DATETIME NOT NULL,
  `name` VARCHAR NOT NULL,
  `user_id` INT NOT NULL
);

-- ---
-- Table 'comment'
-- 
-- ---

DROP TABLE IF EXISTS `comment`;
        
CREATE TABLE `comment` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `created` DATETIME NOT NULL,
  `text` VARCHAR NOT NULL,
  `user_id` INT NOT NULL,
  `post_id` INT NOT NULL
);

-- ---
-- Table 'comment_quote'
-- 
-- ---

DROP TABLE IF EXISTS `comment_quote`;
        
CREATE TABLE `comment_quote` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `quoted` DATETIME NOT NULL,
  `comment_id` INT NOT NULL,
  `order` INT NOT NULL,
  `quotedcomment_id` INT NOT NULL,
  `quotestart` INT NOT NULL,
  `quoteend` INT NOT NULL
);

-- ---
-- Table 'group'
-- 
-- ---

DROP TABLE IF EXISTS `group`;
        
CREATE TABLE `group` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `created` DATETIME NOT NULL,
  `name` VARCHAR NOT NULL
);

-- ---
-- Table 'comment_revision'
-- 
-- ---

DROP TABLE IF EXISTS `comment_revision`;
        
CREATE TABLE `comment_revision` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `revised` DATETIME NOT NULL,
  `changes` VARCHAR NOT NULL,
  `comment_id` INT NOT NULL
);

-- ---
-- Foreign Keys 
-- ---


-- ---
-- Table Properties
-- ---

-- ALTER TABLE `user` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `post` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `comment` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `comment_quote` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `group` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `comment_revision` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `user` (`id`,`created`,`name`) VALUES
-- ('','','');
-- INSERT INTO `post` (`id`,`created`,`name`,`user_id`) VALUES
-- ('','','','');
-- INSERT INTO `comment` (`id`,`created`,`text`,`user_id`,`post_id`) VALUES
-- ('','','','','');
-- INSERT INTO `comment_quote` (`id`,`quoted`,`comment_id`,`order`,`quotedcomment_id`,`quotestart`,`quoteend`) VALUES
-- ('','','','','','','');
-- INSERT INTO `group` (`id`,`created`,`name`) VALUES
-- ('','','');
-- INSERT INTO `comment_revision` (`id`,`revised`,`changes`,`comment_id`) VALUES
-- ('','','','');
'''

lines = script.split("\n")
script = ""
for currentLine in lines:
    if currentLine[:2] != '--':
        script += currentLine
        

commands = script.split(';')

for command in commands:
    command = command.strip()
    db.execute(command)
    print command

db.commit()