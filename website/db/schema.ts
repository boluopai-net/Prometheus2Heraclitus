import { sqliteTable, text, integer, index } from 'drizzle-orm/sqlite-core';
export const rateLimits = sqliteTable('rate_limits', {
  key: text('key').primaryKey(), count: integer('count').notNull(), expiresAt: integer('expires_at').notNull(),
});
export const downloadTokens = sqliteTable('download_tokens', {
  id: text('id').primaryKey(), tokenHash: text('token_hash').notNull().unique(),
  createdAt: text('created_at').notNull(), expiresAt: integer('expires_at').notNull(),
  revokedAt: integer('revoked_at'), label: text('label').notNull(),
},(t)=>[index('download_tokens_created_idx').on(t.createdAt,t.id)]);


export const accessApplications = sqliteTable('access_applications', {
  id: text('id').primaryKey(), capabilityHash: text('capability_hash').notNull(),
  name: text('name').notNull(), contact: text('contact').notNull(), reason: text('reason').notNull(),
  scope: text('scope').notNull(), githubUsername: text('github_username').notNull(),
  status: text('status').notNull().default('submitted'), createdAt: text('created_at').notNull(),
  websiteTokenId: text('website_token_id').references(()=>downloadTokens.id), websiteToken: text('website_token'),
  githubStatus: text('github_status'), reviewedAt: text('reviewed_at'), reviewNote: text('review_note'),
  notificationStatus: text('notification_status').notNull().default('queued'),
  notificationAttempts: integer('notification_attempts').notNull().default(0),
  notificationRetryAt: integer('notification_retry_at').notNull().default(0),
  notificationLease: text('notification_lease'), notificationLeaseUntil: integer('notification_lease_until'),
  notifiedAt: text('notified_at'),
},t=>[index('access_applications_queue_idx').on(t.notificationStatus,t.notificationRetryAt),index('access_applications_review_idx').on(t.status,t.createdAt)]);
