declare namespace Cloudflare {
  interface Env {
    DB?: D1Database;
    BUCKET?: R2Bucket;
    OWNER_EMAIL?: string;
    OWNER_USER_ID?: string;
    HERMES_BRIDGE_KEY?: string;
    CONTENT_PUBLISH_KEY?: string;
  }
}
