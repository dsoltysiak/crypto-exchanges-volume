DROP TABLE IF EXISTS crypto.exchanges;
DROP SCHEMA IF EXISTS crypto;
CREATE SCHEMA crypto;
CREATE TABLE crypto.exchanges (
    id VARCHAR(50),
    name VARCHAR(50),
    rank INT,
    percentTotalVolume NUMERIC(8, 5),
    volumeUsd NUMERIC,
    tradingPairs INT,
    socket BOOLEAN,
    exchangeUrl VARCHAR(50),
    updated_unix_millis BIGINT,
    updated_utc TIMESTAMP
);