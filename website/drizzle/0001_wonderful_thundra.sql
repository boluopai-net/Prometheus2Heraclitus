CREATE TABLE `visitor_messages` (
	`id` text PRIMARY KEY NOT NULL,
	`visitor_id` text NOT NULL,
	`question` text NOT NULL,
	`answer` text,
	`status` text NOT NULL,
	`created_at` integer NOT NULL,
	`lease` text,
	`lease_until` integer,
	FOREIGN KEY (`visitor_id`) REFERENCES `visitors`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `visitor_messages_queue_idx` ON `visitor_messages` (`status`,`created_at`);--> statement-breakpoint
CREATE INDEX `visitor_messages_visitor_idx` ON `visitor_messages` (`visitor_id`,`created_at`);--> statement-breakpoint
CREATE TABLE `visitors` (
	`id` text PRIMARY KEY NOT NULL,
	`key_hash` text NOT NULL,
	`created_at` integer NOT NULL
);
