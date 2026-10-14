CREATE TABLE `download_tokens` (
	`id` text PRIMARY KEY NOT NULL,
	`token_hash` text NOT NULL,
	`created_at` text NOT NULL,
	`expires_at` integer NOT NULL,
	`revoked_at` integer,
	`label` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `download_tokens_token_hash_unique` ON `download_tokens` (`token_hash`);--> statement-breakpoint
CREATE INDEX `download_tokens_created_idx` ON `download_tokens` (`created_at`,`id`);--> statement-breakpoint
CREATE TABLE `rate_limits` (
	`key` text PRIMARY KEY NOT NULL,
	`count` integer NOT NULL,
	`expires_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `suggestions` (
	`id` text PRIMARY KEY NOT NULL,
	`kind` text NOT NULL,
	`title` text NOT NULL,
	`body` text NOT NULL,
	`author` text NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `suggestions_created_idx` ON `suggestions` (`created_at`,`id`);