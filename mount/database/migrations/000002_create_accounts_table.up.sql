CREATE TABLE accounts (
    account_id SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    safe_username VARCHAR(16) GENERATED ALWAYS AS (REPLACE(LOWER(username), ' ', '_')) STORED NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    country CHAR(2) NOT NULL COMMENT 'iso3166-1 alpha-2',
    status VARCHAR(64) NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    created_at DATETIME NOT NULL DEFAULT NOW()
);
