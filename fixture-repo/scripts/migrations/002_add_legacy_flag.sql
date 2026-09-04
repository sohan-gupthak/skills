-- Applied 2023-06-15. Added for the (now-sunset) legacy importer.
-- See commit message on this migration for context.
ALTER TABLE users ADD COLUMN legacy_flag BOOLEAN DEFAULT FALSE;
