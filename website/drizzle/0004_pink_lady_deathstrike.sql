ALTER TABLE `suggestions` ADD `delete_token_hash` text;
--> statement-breakpoint
-- Remove only the duplicate anonymous welcome explicitly selected by the owner.
DELETE FROM `suggestions` WHERE `id` = 'cf171468-4091-4730-b70a-5c85cae9e77b' AND `kind` = 'Philosophy' AND `author` = 'Anonymous' AND `title` = '欢迎一起讨论';
