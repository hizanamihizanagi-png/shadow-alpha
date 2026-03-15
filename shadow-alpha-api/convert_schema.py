import re

sqlite_schema = """
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
        is_active BOOLEAN NOT NULL,
        is_admin BOOLEAN NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (email),
        UNIQUE (phone),
        UNIQUE (promo_code)
)
;
CREATE TABLE tontine_groups (
        name VARCHAR(100) NOT NULL,
        creator_id VARCHAR(36) NOT NULL,
        cycle_type VARCHAR(8) NOT NULL,
        target_amount NUMERIC(18, 2) NOT NULL,
        current_amount NUMERIC(18, 2) NOT NULL,
        status VARCHAR(9) NOT NULL,
        description TEXT,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(creator_id) REFERENCES users (id)
)
;
CREATE TABLE vault_yields (
        cycle_date DATETIME NOT NULL,
        gross_yield NUMERIC(18, 2) NOT NULL,
        performance_fee NUMERIC(18, 2) NOT NULL,
        net_yield NUMERIC(18, 2) NOT NULL,
        strategy_used VARCHAR(100),
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id)
)
;
CREATE TABLE positions (
        user_id VARCHAR(36) NOT NULL,
        sportsbook VARCHAR(100) NOT NULL,
        teams VARCHAR(255) NOT NULL,
        league VARCHAR(100),
        odds NUMERIC(10, 4) NOT NULL,
        stake NUMERIC(18, 2) NOT NULL,
        max_payout NUMERIC(18, 2) NOT NULL,
        current_value NUMERIC(18, 2) NOT NULL,
        current_prob FLOAT,
        time_remaining FLOAT,
        status VARCHAR(9) NOT NULL,
        description TEXT,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE subscriptions (
        user_id VARCHAR(36) NOT NULL,
        "plan" VARCHAR(10) NOT NULL,
        status VARCHAR(9) NOT NULL,
        started_at DATETIME NOT NULL,
        expires_at DATETIME,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE vault_deposits (
        user_id VARCHAR(36) NOT NULL,
        amount NUMERIC(18, 2) NOT NULL,
        status VARCHAR(9) NOT NULL,
        withdrawn_at DATETIME,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE gratitude_tips (
        user_id VARCHAR(36) NOT NULL,
        win_amount NUMERIC(18, 2) NOT NULL,
        tip_pct NUMERIC(5, 2) NOT NULL,
        tip_amount NUMERIC(18, 2) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE prop_fund_trades (
        signal_user_id VARCHAR(36) NOT NULL,
        signal_type VARCHAR(20) NOT NULL,
        direction VARCHAR(14) NOT NULL,
        stake NUMERIC(18, 2) NOT NULL,
        pnl NUMERIC(18, 2) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(signal_user_id) REFERENCES users (id)
)
;
CREATE TABLE user_classifications (
        user_id VARCHAR(36) NOT NULL,
        classification VARCHAR(7) NOT NULL,
        confidence NUMERIC(5, 4) NOT NULL,
        last_updated DATETIME NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE api_keys (
        user_id VARCHAR(36) NOT NULL,
        key_hash VARCHAR(255) NOT NULL,
        key_prefix VARCHAR(20) NOT NULL,
        name VARCHAR(100) NOT NULL,
        tier VARCHAR(10) NOT NULL,
        usage_count INTEGER NOT NULL,
        is_active BOOLEAN NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id),
        UNIQUE (key_hash)
)
;
CREATE TABLE promo_codes (
        code VARCHAR(30) NOT NULL,
        creator_id VARCHAR(36) NOT NULL,
        uses_remaining INTEGER NOT NULL,
        commission_rate NUMERIC(5, 2) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(creator_id) REFERENCES users (id)
)
;
CREATE TABLE orders (
        position_id VARCHAR(36) NOT NULL,
        seller_id VARCHAR(36) NOT NULL,
        buyer_id VARCHAR(36),
        order_type VARCHAR(4) NOT NULL,
        price NUMERIC(18, 2) NOT NULL,
        status VARCHAR(16) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(seller_id) REFERENCES users (id),
        FOREIGN KEY(buyer_id) REFERENCES users (id)
)
;
CREATE TABLE tontine_members (
        group_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        role VARCHAR(7) NOT NULL,
        contribution_total NUMERIC(18, 2) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(group_id) REFERENCES tontine_groups (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE tontine_contributions (
        group_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        amount NUMERIC(18, 2) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(group_id) REFERENCES tontine_groups (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE shield_contracts (
        position_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        premium_paid NUMERIC(18, 2) NOT NULL,
        coverage_pct NUMERIC(5, 2) NOT NULL,
        hedge_id VARCHAR(100),
        status VARCHAR(7) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE position_loans (
        position_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        loan_amount NUMERIC(18, 2) NOT NULL,
        collateral_value NUMERIC(18, 2) NOT NULL,
        fee NUMERIC(18, 2) NOT NULL,
        status VARCHAR(10) NOT NULL,
        repaid_at DATETIME,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE instant_cashouts (
        position_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        fair_value NUMERIC(18, 2) NOT NULL,
        offered_price NUMERIC(18, 2) NOT NULL,
        spread_pct NUMERIC(5, 2) NOT NULL,
        status VARCHAR(9) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(position_id) REFERENCES positions (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
)
;
CREATE TABLE referrals (
        promo_code_id VARCHAR(36) NOT NULL,
        referred_user_id VARCHAR(36) NOT NULL,
        lifetime_revenue NUMERIC(18, 2) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(promo_code_id) REFERENCES promo_codes (id),
        UNIQUE (referred_user_id),
        FOREIGN KEY(referred_user_id) REFERENCES users (id)
)
;
CREATE TABLE trades (
        order_id VARCHAR(36) NOT NULL,
        buyer_id VARCHAR(36) NOT NULL,
        seller_id VARCHAR(36) NOT NULL,
        price NUMERIC(18, 2) NOT NULL,
        fee NUMERIC(18, 2) NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(order_id) REFERENCES orders (id),
        FOREIGN KEY(buyer_id) REFERENCES users (id),
        FOREIGN KEY(seller_id) REFERENCES users (id)
)
;
CREATE TABLE shield_claims (
        contract_id VARCHAR(36) NOT NULL,
        payout_amount NUMERIC(18, 2) NOT NULL,
        claimed_at DATETIME NOT NULL,
        id VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(contract_id) REFERENCES shield_contracts (id)
)
"""

# Transformations
pg_schema = sqlite_schema.replace("DATETIME", "TIMESTAMP WITH TIME ZONE")
pg_schema = pg_schema.replace("VARCHAR(36)", "UUID")
pg_schema = pg_schema.replace("FLOAT", "DOUBLE PRECISION")
pg_schema = pg_schema.replace("BOOLEAN NOT NULL", "BOOLEAN DEFAULT false NOT NULL")

# Extract table names
table_names = re.findall(r"CREATE TABLE ([a-z_]+)", sqlite_schema)

rls_policies = "\n\n-- RLS POLICIES\n"
for table in table_names:
    rls_policies += f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;\n"
    # Basic select policy
    rls_policies += f"CREATE POLICY \"Enable read access for authenticated users\" ON {table} FOR SELECT USING (true);\n"
    # Basic insert policy
    rls_policies += f"CREATE POLICY \"Enable insert for authenticated users\" ON {table} FOR INSERT WITH CHECK (true);\n"
    # Basic update policy
    rls_policies += f"CREATE POLICY \"Enable update for authenticated users\" ON {table} FOR UPDATE USING (true);\n"
    # Basic delete policy
    rls_policies += f"CREATE POLICY \"Enable delete for authenticated users\" ON {table} FOR DELETE USING (true);\n"
    rls_policies += "\n"

full_sql = pg_schema + rls_policies
with open("shadow_alpha_pg_migration.sql", "w") as f:
    f.write(full_sql)

print(full_sql)
