
CREATE TABLE users (
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(20),
        display_name VARCHAR(100) NOT NULL,
        hashed_password TEXT NOT NULL,
        tier VARCHAR(10) NOT NULL,
        kyc_status VARCHAR(10) NOT NULL,
        promo_code VARCHAR(20),
        referred_by VARCHAR(20),
        wallet_balance NUMERIC NOT NULL,
        is_active BOOLEAN DEFAULT false NOT NULL,
        is_admin BOOLEAN DEFAULT false NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (email),
        UNIQUE (phone),
        UNIQUE (promo_code)
)
;
CREATE TABLE tontine_groups (
        name VARCHAR(100) NOT NULL,
        creator_id UUID NOT NULL,
        cycle_type VARCHAR(8) NOT NULL,
        target_amount NUMERIC(18, 2) NOT NULL,
        current_amount NUMERIC(18, 2) NOT NULL,
        status VARCHAR(9) NOT NULL,
        description TEXT,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(creator_id) REFERENCES users (id)
)
;
CREATE TABLE vault_yields (
        cycle_date TIMESTAMP WITH TIME ZONE NOT NULL,
        gross_yield NUMERIC(18, 2) NOT NULL,
        performance_fee NUMERIC(18, 2) NOT NULL,
        net_yield NUMERIC(18, 2) NOT NULL,
        strategy_used VARCHAR(100),
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id)
)
;
CREATE TABLE positions (
        user_id UUID NOT NULL,
        sportsbook VARCHAR(100) NOT NULL,
        teams VARCHAR(255) NOT NULL,
        league VARCHAR(100),
        odds NUMERIC(10, 4) NOT NULL,
        stake NUMERIC(18, 2) NOT NULL,
        max_payout NUMERIC(18, 2) NOT NULL,
        current_value NUMERIC(18, 2) NOT NULL,
        current_prob DOUBLE PRECISION,
        time_remaining DOUBLE PRECISION,
        status VARCHAR(9) NOT NULL,
        description TEXT,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE subscriptions (
        user_id UUID NOT NULL,
        "plan" VARCHAR(10) NOT NULL,
        status VARCHAR(9) NOT NULL,
        started_at TIMESTAMP WITH TIME ZONE NOT NULL,
        expires_at TIMESTAMP WITH TIME ZONE,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE vault_deposits (
        user_id UUID NOT NULL,
        amount NUMERIC(18, 2) NOT NULL,
        status VARCHAR(9) NOT NULL,
        withdrawn_at TIMESTAMP WITH TIME ZONE,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE gratitude_tips (
        user_id UUID NOT NULL,
        win_amount NUMERIC(18, 2) NOT NULL,
        tip_pct NUMERIC(5, 2) NOT NULL,
        tip_amount NUMERIC(18, 2) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE prop_fund_trades (
        signal_user_id UUID NOT NULL,
        signal_type VARCHAR(20) NOT NULL,
        direction VARCHAR(14) NOT NULL,
        stake NUMERIC(18, 2) NOT NULL,
        pnl NUMERIC(18, 2) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(signal_user_id) REFERENCES users (id)
)
;
CREATE TABLE user_classifications (
        user_id UUID NOT NULL,
        classification VARCHAR(7) NOT NULL,
        confidence NUMERIC(5, 4) NOT NULL,
        last_updated TIMESTAMP WITH TIME ZONE NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE api_keys (
        user_id UUID NOT NULL,
        key_hash VARCHAR(255) NOT NULL,
        key_prefix VARCHAR(20) NOT NULL,
        name VARCHAR(100) NOT NULL,
        tier VARCHAR(10) NOT NULL,
        usage_count INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT false NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id),
        UNIQUE (key_hash)
)
;
CREATE TABLE promo_codes (
        code VARCHAR(30) NOT NULL,
        creator_id UUID NOT NULL,
        uses_remaining INTEGER NOT NULL,
        commission_rate NUMERIC(5, 2) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(creator_id) REFERENCES users (id)
)
;
CREATE TABLE orders (
        position_id UUID NOT NULL,
        seller_id UUID NOT NULL,
        buyer_id UUID,
        order_type VARCHAR(4) NOT NULL,
        price NUMERIC(18, 2) NOT NULL,
        status VARCHAR(16) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(seller_id) REFERENCES users (id),
        FOREIGN KEY(buyer_id) REFERENCES users (id)
)
;
CREATE TABLE tontine_members (
        group_id UUID NOT NULL,
        user_id UUID NOT NULL,
        role VARCHAR(7) NOT NULL,
        contribution_total NUMERIC(18, 2) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(group_id) REFERENCES tontine_groups (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE tontine_contributions (
        group_id UUID NOT NULL,
        user_id UUID NOT NULL,
        amount NUMERIC(18, 2) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(group_id) REFERENCES tontine_groups (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE shield_contracts (
        position_id UUID NOT NULL,
        user_id UUID NOT NULL,
        premium_paid NUMERIC(18, 2) NOT NULL,
        coverage_pct NUMERIC(5, 2) NOT NULL,
        hedge_id VARCHAR(100),
        status VARCHAR(7) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE position_loans (
        position_id UUID NOT NULL,
        user_id UUID NOT NULL,
        loan_amount NUMERIC(18, 2) NOT NULL,
        collateral_value NUMERIC(18, 2) NOT NULL,
        fee NUMERIC(18, 2) NOT NULL,
        status VARCHAR(10) NOT NULL,
        repaid_at TIMESTAMP WITH TIME ZONE,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE instant_cashouts (
        position_id UUID NOT NULL,
        user_id UUID NOT NULL,
        fair_value NUMERIC(18, 2) NOT NULL,
        offered_price NUMERIC(18, 2) NOT NULL,
        spread_pct NUMERIC(5, 2) NOT NULL,
        status VARCHAR(9) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE referrals (
        promo_code_id UUID NOT NULL,
        referred_user_id UUID NOT NULL,
        lifetime_revenue NUMERIC(18, 2) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(promo_code_id) REFERENCES promo_codes (id),
        UNIQUE (referred_user_id),
        FOREIGN KEY(referred_user_id) REFERENCES users (id)
)
;
CREATE TABLE trades (
        order_id UUID NOT NULL,
        buyer_id UUID NOT NULL,
        seller_id UUID NOT NULL,
        price NUMERIC(18, 2) NOT NULL,
        fee NUMERIC(18, 2) NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(order_id) REFERENCES orders (id),
        FOREIGN KEY(buyer_id) REFERENCES users (id),
        FOREIGN KEY(seller_id) REFERENCES users (id)
)
;
CREATE TABLE shield_claims (
        contract_id UUID NOT NULL,
        payout_amount NUMERIC(18, 2) NOT NULL,
        claimed_at TIMESTAMP WITH TIME ZONE NOT NULL,
        id UUID NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(contract_id) REFERENCES shield_contracts (id)
)


-- RLS POLICIES
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON users FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON users FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON users FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON users FOR DELETE USING (true);

ALTER TABLE tontine_groups ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON tontine_groups FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON tontine_groups FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON tontine_groups FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON tontine_groups FOR DELETE USING (true);

ALTER TABLE vault_yields ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON vault_yields FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON vault_yields FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON vault_yields FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON vault_yields FOR DELETE USING (true);

ALTER TABLE positions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON positions FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON positions FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON positions FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON positions FOR DELETE USING (true);

ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON subscriptions FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON subscriptions FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON subscriptions FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON subscriptions FOR DELETE USING (true);

ALTER TABLE vault_deposits ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON vault_deposits FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON vault_deposits FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON vault_deposits FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON vault_deposits FOR DELETE USING (true);

ALTER TABLE gratitude_tips ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON gratitude_tips FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON gratitude_tips FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON gratitude_tips FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON gratitude_tips FOR DELETE USING (true);

ALTER TABLE prop_fund_trades ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON prop_fund_trades FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON prop_fund_trades FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON prop_fund_trades FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON prop_fund_trades FOR DELETE USING (true);

ALTER TABLE user_classifications ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON user_classifications FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON user_classifications FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON user_classifications FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON user_classifications FOR DELETE USING (true);

ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON api_keys FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON api_keys FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON api_keys FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON api_keys FOR DELETE USING (true);

ALTER TABLE promo_codes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON promo_codes FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON promo_codes FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON promo_codes FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON promo_codes FOR DELETE USING (true);

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON orders FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON orders FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON orders FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON orders FOR DELETE USING (true);

ALTER TABLE tontine_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON tontine_members FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON tontine_members FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON tontine_members FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON tontine_members FOR DELETE USING (true);

ALTER TABLE tontine_contributions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON tontine_contributions FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON tontine_contributions FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON tontine_contributions FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON tontine_contributions FOR DELETE USING (true);

ALTER TABLE shield_contracts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON shield_contracts FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON shield_contracts FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON shield_contracts FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON shield_contracts FOR DELETE USING (true);

ALTER TABLE position_loans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON position_loans FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON position_loans FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON position_loans FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON position_loans FOR DELETE USING (true);

ALTER TABLE instant_cashouts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON instant_cashouts FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON instant_cashouts FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON instant_cashouts FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON instant_cashouts FOR DELETE USING (true);

ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON referrals FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON referrals FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON referrals FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON referrals FOR DELETE USING (true);

ALTER TABLE trades ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON trades FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON trades FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON trades FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON trades FOR DELETE USING (true);

ALTER TABLE shield_claims ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for authenticated users" ON shield_claims FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON shield_claims FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON shield_claims FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON shield_claims FOR DELETE USING (true);

