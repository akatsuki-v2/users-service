CREATE TABLE stats (
    account_id INT NOT NULL,
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
    created_at DATETIME NOT NULL DEFAULT NOW(),
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (account_id, game_mode)
);
