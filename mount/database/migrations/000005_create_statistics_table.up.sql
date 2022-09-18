CREATE TABLE statistics (
    account_id INTEGER NOT NULL,
    game_mode SMALLINT NOT NULL,
    total_score BIGINT NOT NULL,
    ranked_score BIGINT NOT NULL,
    performance INT NOT NULL,
    play_count INT NOT NULL,
    play_time INT NOT NULL,
    accuracy REAL NOT NULL,
    max_combo INT NOT NULL,
    total_hits INT NOT NULL,
    replay_views INT NOT NULL,
    xh_count INT NOT NULL,
    x_count INT NOT NULL,
    sh_count INT NOT NULL,
    s_count INT NOT NULL,
    a_count INT NOT NULL,
    status VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    PRIMARY KEY (account_id, game_mode)
);