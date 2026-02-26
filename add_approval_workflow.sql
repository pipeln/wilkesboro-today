-- Add approval workflow columns to news_raw table

-- Add approval status column
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS approval_status TEXT DEFAULT 'pending';

-- Add telegram notification sent flag
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS telegram_notified BOOLEAN DEFAULT false;

-- Add telegram message ID for tracking
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS telegram_message_id TEXT;

-- Add reviewed by column
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS reviewed_by TEXT;

-- Add reviewed at timestamp
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;

-- Add notes for reviewer
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS reviewer_notes TEXT;

-- Create index for pending approvals
CREATE INDEX IF NOT EXISTS idx_news_raw_approval ON news_raw(approval_status) WHERE approval_status = 'pending';

-- Create index for telegram notifications
CREATE INDEX IF NOT EXISTS idx_news_raw_telegram ON news_raw(telegram_notified) WHERE telegram_notified = false;
