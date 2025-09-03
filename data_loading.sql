CREATE TABLE ads_spends (
    date DATE,
    platform TEXT,
    account TEXT,
    campaign TEXT,
    country TEXT,
    device TEXT,
    spend NUMERIC,
    clicks INT,
    impressions INT,
    conversions INT,
    load_date TIMESTAMP,
    source_file_name TEXT
);
select * from ads_spends;
