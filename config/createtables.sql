CREATE TABLE IF NOT EXISTS `persistence` (
	`key`	TEXT,
	`value`	TEXT
);
INSERT INTO `persistence`(`key`, `value`) VALUES ("last_tweet", "753076611352756228");

CREATE TABLE IF NOT EXISTS `update_channels` (
	`server_id` TEXT,
	`channel_id` TEXT
);
INSERT INTO `update_channels` (`server_id`, `channel_id`) VALUES ("154261963692703745", "169500338494111744");