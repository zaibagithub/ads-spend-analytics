from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import psycopg2
import os


client = OpenAI(api_key="xxxx")  

app = FastAPI()

class NLQuery(BaseModel):
    question: str

@app.post("/nl2sql")
async def nl2sql(query: NLQuery):
    prompt = f"""


        You are an assistant that converts natural language to SQL for PostgreSQL.
        Given the table 'ads_spends' with columns: date, spend, revenue, customers_acquired, conversions.

        Also some terms to derive,

        CAC = spend / conversions
        ROAS = (revenue / spend), where assume revenue = conversions × 100

        Question: {query.question}
        SQL:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    
    if not sql.lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed", "sql": sql}

    try:
        # Connects to Supabase
        conn = psycopg2.connect(
            host="aws-1-ap-south-1.pooler.supabase.com",
            user="postgres.uizrztdnajkqpqlbtglt",
            password="Thabassum@2004",
            dbname="postgres",
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        return {"error": str(e), "sql": sql}

    # converts results back to NL
    sql_prompt = f"""
        You are an assistant that converts SQL query results into natural language.
        The table is 'ads_spends' with columns:
        date, spend, clicks, impressions, conversions (and derived revenue = conversions*100).

        Question: {query.question}
        Rows: {rows}
        Answer in plain English:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": sql_prompt}],
        temperature=0
    )

    answer = response.choices[0].message.content.strip()

    return {
        "sql": sql,
        "rows": rows,
        "NL_answer": answer
    }
