-- ============================================================================
-- COMPLETE SCHEMA: Vue Money Transactions Table
-- Reference implementation following ALL Architect principles
-- ============================================================================

CREATE TABLE transactions (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Foreign Keys
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  
  -- Flinks Integration
  flinks_transaction_id TEXT UNIQUE NOT NULL,
  flinks_account_id TEXT NOT NULL,
  
  -- Core Transaction Fields
  amount DECIMAL(12,2) NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CAD',
  transaction_date DATE NOT NULL,
  post_date DATE,
  
  -- Merchant Information
  raw_description TEXT NOT NULL,
  cleaned_merchant_name TEXT,
  merchant_category TEXT,
  merchant_logo_url TEXT,
  
  -- Three-Layer Categorization System
  flinks_category TEXT,
  auto_category TEXT,
  user_category TEXT,
  category_confidence DECIMAL(3,2) CHECK (category_confidence BETWEEN 0 AND 1),
  
  -- Transaction Classification Flags
  is_internal_transfer BOOLEAN DEFAULT FALSE,
  is_subscription BOOLEAN DEFAULT FALSE,
  is_anomaly BOOLEAN DEFAULT FALSE,
  is_pending BOOLEAN DEFAULT FALSE,
  
  -- Metadata
  raw_data JSONB,
  tags TEXT[],
  notes TEXT,
  
  -- Audit Fields
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ,
  
  -- Constraints
  CONSTRAINT valid_amount CHECK (amount != 0),
  CONSTRAINT valid_currency CHECK (currency IN ('CAD', 'USD', 'EUR', 'GBP')),
  CONSTRAINT valid_dates CHECK (transaction_date <= post_date OR post_date IS NULL)
);

-- ============================================================================
-- Indexes (Created CONCURRENTLY in production)
-- ============================================================================

CREATE INDEX CONCURRENTLY idx_transactions_user_id 
ON transactions(user_id) WHERE deleted_at IS NULL;

CREATE INDEX CONCURRENTLY idx_transactions_account_id 
ON transactions(account_id);

CREATE INDEX CONCURRENTLY idx_transactions_date 
ON transactions(transaction_date DESC);

CREATE INDEX CONCURRENTLY idx_transactions_user_date 
ON transactions(user_id, transaction_date DESC) WHERE deleted_at IS NULL;

CREATE INDEX CONCURRENTLY idx_transactions_category 
ON transactions(user_id, COALESCE(user_category, auto_category, flinks_category)) 
WHERE deleted_at IS NULL;

CREATE UNIQUE INDEX idx_transactions_flinks_unique 
ON transactions(flinks_transaction_id);

CREATE INDEX CONCURRENTLY idx_transactions_subscriptions 
ON transactions(user_id, cleaned_merchant_name) 
WHERE is_subscription = TRUE AND deleted_at IS NULL;

-- ============================================================================
-- Trigger
-- ============================================================================

CREATE TRIGGER update_transactions_updated_at
  BEFORE UPDATE ON transactions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- RLS Policies
-- ============================================================================

ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "transactions_select_own"
  ON transactions FOR SELECT TO authenticated
  USING (auth.uid() = user_id AND deleted_at IS NULL);

CREATE POLICY "transactions_insert_own"
  ON transactions FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "transactions_update_own"
  ON transactions FOR UPDATE TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "transactions_delete_own"
  ON transactions FOR DELETE TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "transactions_service_role_all"
  ON transactions FOR ALL TO service_role
  USING (true) WITH CHECK (true);

GRANT SELECT, INSERT, UPDATE ON transactions TO authenticated;
GRANT ALL ON transactions TO service_role;

-- ============================================================================
-- Comments
-- ============================================================================

COMMENT ON TABLE transactions IS 'Financial transactions from linked bank accounts via Flinks';
COMMENT ON COLUMN transactions.user_category IS 'User override - highest priority';
COMMENT ON COLUMN transactions.raw_data IS 'Full Flinks response for debugging';
