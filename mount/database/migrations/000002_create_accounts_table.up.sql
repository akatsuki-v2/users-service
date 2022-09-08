CREATE TABLE accounts (
    rec_id INT NOT NULL PRIMARY KEY,
    account_id char(36) NOT NULL UNIQUE,
    username varchar(16) NOT NULL,
    safe_username varchar(16) AS (REPLACE(LOWER(username), ' ', '_')) NOT NULL,
    email_address varchar(255) NOT NULL,
    country char(2) NOT NULL COMMENT 'iso3166-1 alpha-2',
    status varchar(64) NOT NULL,
    updated_at datetime NOT NULL DEFAULT NOW(),
    created_at datetime NOT NULL DEFAULT NOW()
);
