CREATE SCHEMA `duang` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;

CREATE TABLE `duang`.`spider` (
  `id` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NULL,
  `type` VARCHAR(255) NULL,
  `publishDate` DATE NULL,
  `endDate` DATE NULL,
  `contact` VARCHAR(255) NULL,
  `url` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
