CREATE TABLE accounts (
    rec_id INT NOT NULL PRIMARY KEY,
    account_id CHAR(36) NOT NULL UNIQUE,
    username VARCHAR(16) NOT NULL,
    safe_username VARCHAR(16) AS (REPLACE(LOWER(username), ' ', '_')) NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    country CHAR(2) NOT NULL COMMENT 'iso3166-1 alpha-2',
    status VARCHAR(64) NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    created_at DATETIME NOT NULL DEFAULT NOW()
);
