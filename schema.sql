CREATE TABLE `requirements` (
  `req_id` integer PRIMARY KEY,
  `object_id` integer COMMENT 'Foreign Key',
  `type` integer,
  `value` integer
);

CREATE TABLE `objects` (
  `id` integer PRIMARY KEY,
  `name` text,
  `effect` text
);

CREATE TABLE `traits` (
  `id` integer PRIMARY KEY COMMENT 'Foreign Key',
  `dice` integer
);

CREATE TABLE `spells` (
  `id` integer PRIMARY KEY,
  `name` text,
  `effect` text,
  `dice` integer,
  `level` integer
);

CREATE TABLE `spell_tags` (
  `spell_id` integer,
  `name` integer
);

CREATE TABLE `items` (
  `id` integer PRIMARY KEY COMMENT 'Foreign Key',
  `cost` integer,
  `craft` integer
);

CREATE TABLE `item_tags` (
  `item_id` integer,
  `name` integer,
  `value` integer
);

ALTER TABLE `requirements` ADD FOREIGN KEY (`object_id`) REFERENCES `objects` (`id`);

ALTER TABLE `items` ADD FOREIGN KEY (`id`) REFERENCES `objects` (`id`);

ALTER TABLE `traits` ADD FOREIGN KEY (`id`) REFERENCES `objects` (`id`);

ALTER TABLE `spell_tags` ADD FOREIGN KEY (`spell_id`) REFERENCES `spells` (`id`);

ALTER TABLE `item_tags` ADD FOREIGN KEY (`item_id`) REFERENCES `items` (`id`);
