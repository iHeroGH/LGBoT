CREATE TABLE IF NOT EXISTS guild_settings(
    guild_id BIGINT PRIMARY KEY,
    prefix VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS aliases(
    guild_id BIGINT,
    alias VARCHAR(30),
    actual_topic VARCHAR(100),
    PRIMARY KEY (guild_id, alias)
);

CREATE TABLE IF NOT EXISTS user_settings(
    user_id BIGINT PRIMARY KEY
);