CREATE TABLE `access_applications` (
	`id` text PRIMARY KEY NOT NULL,
	`capability_hash` text NOT NULL,
	`name` text NOT NULL,
	`contact` text NOT NULL,
	`reason` text NOT NULL,
	`scope` text NOT NULL,
	`github_username` text NOT NULL,
	`status` text DEFAULT 'submitted' NOT NULL,
	`created_at` text NOT NULL,
	`website_token_id` text,
	`website_token` text,
	`github_status` text,
	`reviewed_at` text,
	`review_note` text,
	`notification_status` text DEFAULT 'queued' NOT NULL,
	`notification_attempts` integer DEFAULT 0 NOT NULL,
	`notification_retry_at` integer DEFAULT 0 NOT NULL,
	`notification_lease` text,
	`notification_lease_until` integer,
	`notified_at` text,
	FOREIGN KEY (`website_token_id`) REFERENCES `download_tokens`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `access_applications_queue_idx` ON `access_applications` (`notification_status`,`notification_retry_at`);--> statement-breakpoint
CREATE INDEX `access_applications_review_idx` ON `access_applications` (`status`,`created_at`);