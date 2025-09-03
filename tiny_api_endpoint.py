from fastapi import FastAPI, Query
import psycopg2
import os

app = FastAPI()

@app.get("/metrics")
async def metrics(start: str = Query(...), end: str = Query(...)):
    try:
        # Connects to Supabase
        conn = psycopg2.connect(
               host="aws-1-ap-south-1.pooler.supabase.com",
                port="5432",
                user="postgres.uizrztdnajkqpqlbtglt",
                password="Thabassum@2004",
                dbname="postgres",
                sslmode="require"
        )

        cur = conn.cursor()
        query = """
        SELECT 
            SUM(spend) AS spend,
            SUM(conversions) AS conversions,
            ROUND(SUM(spend) / NULLIF(SUM(conversions),0), 2) AS CAC,
            ROUND((SUM(conversions) * 100.0) / NULLIF(SUM(spend),0), 2) AS ROAS
        FROM ads_spends
        WHERE date BETWEEN %s AND %s;
        """
        cur.execute(query, (start, end))
        result = cur.fetchone()
        cur.close()
        conn.close()

        return {
            "start_date": start,
            "end_date": end,
            "spend": float(result[0] or 0),
            "conversions": int(result[1] or 0),
            "CAC": float(result[2] or 0),
            "ROAS": float(result[3] or 0)
        }
    except Exception as e:
        return {"error": str(e)}
