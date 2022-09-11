CREATE TABLE credentials (
    rec_id SERIAL NOT NULL PRIMARY KEY,
    credentials_id UUID NOT NULL UNIQUE,
    account_id INT NOT NULL,
    identifier_type TEXT NOT NULL,
    identifier TEXT NOT NULL,
    passphrase TEXT NOT NULL,
    status VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
