CREATE OR REPLACE VIEW kpi_metrics AS
WITH bounds AS (
    -- To get latest date from the DB
    SELECT MAX(date) AS max_date FROM ads_spends
),
last30 AS (
    SELECT
        SUM(spend) AS spend,
        SUM(conversions) AS conversions
    FROM ads_spends, bounds
    WHERE date BETWEEN bounds.max_date - INTERVAL '29 days' AND bounds.max_date
),
prev30 AS (
    SELECT
        SUM(spend) AS spend,
        SUM(conversions) AS conversions
    FROM ads_spends, bounds
    WHERE date BETWEEN bounds.max_date - INTERVAL '59 days'
                  AND bounds.max_date - INTERVAL '30 days'
)
SELECT
    l.spend AS last30_spend,
    p.spend AS prev30_spend,
    ROUND(100.0 * (l.spend - p.spend) / NULLIF(p.spend,0), 2) AS spend_delta_pct,

    (l.spend / NULLIF(l.conversions,0)) AS last30_cac,
    (p.spend / NULLIF(p.conversions,0)) AS prev30_cac,
    ROUND(100.0 * ((l.spend/NULLIF(l.conversions,1)) - (p.spend/NULLIF(p.conversions,1)))
        / NULLIF((p.spend/NULLIF(p.conversions,1)),0), 2) AS cac_delta_pct,

    ((l.conversions*100.0) / NULLIF(l.spend,0)) AS last30_roas,
    ((p.conversions*100.0) / NULLIF(p.spend,0)) AS prev30_roas,
    ROUND(100.0 * (((l.conversions*100.0)/NULLIF(l.spend,0)) - ((p.conversions*100.0)/NULLIF(p.spend,0)))
        / NULLIF(((p.conversions*100.0)/NULLIF(p.spend,0)),0), 2) AS roas_delta_pct
FROM last30 l, prev30 p;

SELECT MAX(date), MIN(date) FROM ads_spends;

SELECT * FROM kpi_metrics;
