
CREATE TABLE `requirements` (
  `req_id` integer PRIMARY KEY AUTO_INCREMENT, 
  `object_id` integer COMMENT 'Foreign Key',
  `type` text COMMENT 'Body,Mind,Soul,Arcana,Charm,Crafting,Medicine,Nature,Thieving',
  `value` integer
);

CREATE TABLE `objects` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` text,
  `effect` text,
  `times_selected` integer DEFAULT 0
);

CREATE TABLE `traits` (
  `id` integer PRIMARY KEY COMMENT 'Foreign Key',
  `dice` integer COMMENT 'Dice cost (0-4)',
  `is_passive` bool COMMENT 'Is a Passive, used as a suport for assisting in difrences between Pure passives and action passives'
);

CREATE TABLE `spells` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` text,
  `effect` text,
  `dice` integer COMMENT 'Number of dice for cast (1-3)',
  `level` integer COMMENT 'Strain Cost (0-10)'
);

CREATE TABLE `spell_tags` (
  `tag_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `spell_id` integer COMMENT 'Foreign Key',
  `name` text COMMENT 'AOE,Attack,CC,Damage,Focus,Ranged,Touch,Utility'
);

CREATE TABLE `items` (
  `id` integer PRIMARY KEY COMMENT 'Foreign Key',
  `cost` integer COMMENT 'Gold Cost to buy' DEFAULT 0,
  `craft` integer COMMENT 'Crafting Cost' DEFAULT 0
);

CREATE TABLE `item_tags` (
  `tag_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `item_id` integer COMMENT 'Foreign Key',
  `name` text,
  `value` integer DEFAULT 0
);

CREATE TABLE `users` (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`discord_id` TEXT NOT NULL,
	`name` TEXT NULL DEFAULT NULL,
	`is_admin` TINYINT(1) NOT NULL DEFAULT '0',
	`email` TEXT NULL DEFAULT NULL
);

CREATE TABLE `creatures` (
	`id` INTEGER PRIMARY KEY AUTO_INCREMENT,
	`name` TEXT NOT NULL,
    `level` integer DEFAULT 0,
    `body` integer DEFAULT 0,
    `mind` integer DEFAULT 0,
    `soul` integer DEFAULT 0,
    `arcana` integer DEFAULT 0,
    `crafting` integer DEFAULT 0,
    `charm` integer DEFAULT 0,
    `thieving` integer DEFAULT 0,
    `nature` integer DEFAULT 0,
    `medicine` integer DEFAULT 0,
	`traits` TEXT NULL DEFAULT NULL,
    `spells` TEXT NULL DEFAULT NULL,
    `items` TEXT NULL DEFAULT NULL,
    `notes` TEXT NULL DEFAULT NULL
);

CREATE TABLE `creature_types` (
  `type_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `creature_id` integer COMMENT 'Foreign Key',
  `name` text COMMENT 'player, humanoid, animal, undead, construct, monstrosity, planar, mythic'
);

CREATE TABLE `creature_tags` (
  `tag_id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `creature_id` integer COMMENT 'Foreign Key',
  `name` text,
  `value` integer DEFAULT 0
);

ALTER TABLE `requirements` ADD FOREIGN KEY (`object_id`) REFERENCES `objects` (`id`);

ALTER TABLE `items` ADD FOREIGN KEY (`id`) REFERENCES `objects` (`id`);

ALTER TABLE `traits` ADD FOREIGN KEY (`id`) REFERENCES `objects` (`id`);

ALTER TABLE `spell_tags` ADD FOREIGN KEY (`spell_id`) REFERENCES `spells` (`id`);

ALTER TABLE `item_tags` ADD FOREIGN KEY (`item_id`) REFERENCES `items` (`id`);

ALTER TABLE `creature_types` ADD FOREIGN KEY (`creature_id`) REFERENCES `creatures` (`id`);
ALTER TABLE `creature_tags` ADD FOREIGN KEY (`creature_id`) REFERENCES `creatures` (`id`);


INSERT INTO objects (id,name, effect) VALUES (1, "Kokk", "This is here so that we can do testing.");