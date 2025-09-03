# ads-spend-analytics

## Description
Automated advertising spend pipeline that collects data using n8n, persists it in Supabase, models key metrics such as CAC and ROAS, and     exposes insights via a FastAPI API for easy access.

## Features

- **Automated Data Ingestion:** Uses [n8n](https://n8n.io/) to load ad spend data into PostgreSQL (Supabase).  
- **Data Storage:** Stores raw and processed ad spend data with provenance fields (`load_date`, `source_file_name`).  
- **KPI Modeling:** Computes marketing metrics such as:
  - **CAC (Customer Acquisition Cost) = spend / conversions**
  - **ROAS (Return on Ad Spend) = (conversions × 100) / spend**
- **Comparison:** Last 30 days vs previous 30 days with absolute values and percentage deltas.  
- **APIs:**  
  - `/metrics` – Returns aggregated metrics (spend, conversions, CAC, ROAS) for a given date range.  
  - `/nl2sql` – Converts natural language questions into SQL queries, executes them safely, and returns results in plain English.

## Tech Stacks used

Python & FastAPI – API development
PostgreSQL (Supabase) – Database
n8n – Workflow automation for data ingestion
OpenAI GPT-3.5 – Natural language to SQL conversion 
 

## Table Structure

**`ads_spends` Table**  

| Column           | Type      | Description                                     |
|-----------------|-----------|-------------------------------------------------|
| date            | DATE      | Date of the campaign                            |
| platform        | TEXT      | Advertising platform                            |
| account         | TEXT      | Account name                                    |
| campaign        | TEXT      | Campaign name                                   |
| country         | TEXT      | Country targeted                                |
| device          | TEXT      | Device type                                     |
| spend           | NUMERIC   | Amount spent                                    |
| clicks          | INT       | Number of clicks                                |
| impressions     | INT       | Number of impressions                           |
| conversions     | INT       | Number of conversions                           |
| load_date       | TIMESTAMP | Timestamp when the record was ingested          |
| source_file_name| TEXT      | Original CSV file name                          |



## KPI Modelling

The SQL view `kpi_metrics` calculates key advertising performance metrics for the last 30 days and compares them with the previous 30 days.  

**KPIs Calculated:**  
- **Spend** – Total ad spend over the period  
- **CAC (Customer Acquisition Cost)** = spend / conversions  
- **ROAS (Return on Ad Spend)** = (conversions × 100) / spend  
- **Delta (%)** – Percentage change between last 30 days and previous 30 days
  

## Exposing Metrics

Returns aggregated advertising metrics (spend, conversions, CAC, ROAS) for a specified date range. This endpoint exposes key insights to analysts or stakeholders. This endpoint is the main way to expose KPIs and metrics from the ads spend data to external tools, dashboards, or stakeholders.

**Query Parameters:**  
- `start` – Start date (`YYYY-MM-DD`)  
- `end` – End date (`YYYY-MM-DD`)
  
**Example Request:**  
GET /metrics?start=2025-08-01&end=2025-08-31

**Example Response**  
``json
{
  "start_date": "2025-08-01",
  "end_date": "2025-08-31",
  "spend": 1000.0,
  "conversions": 50,
  "CAC": 20.0,
  "ROAS": 5.0
}


## API Documentation

**Converts natural language questions into SQL, executes safely, and returns results in plain English.**

**Sample request body**
{
  "question": "What was the total spend and CAC for August 2025?"
}

**Example Response**
{
  "sql": "SELECT SUM(spend), SUM(spend)/SUM(conversions) AS CAC FROM ads_spends WHERE date BETWEEN '2025-08-01' AND '2025-08-31';",
  "rows": [[1000.0, 20.0]],
  "NL_answer": "The total spend for August 2025 was 1000.0 and the CAC was 20.0."
}


## Installation & Setup

1. Clone the repository:  
``bash
      git clone <repo_url>
      cd ads-spend-analytics

2. Install dependencies:
   
       pip install -r requirements.txt

3. Setup database connection in your FastAPI code (update host, user, password, dbname).

4. Run the FastAPI server:
   
       uvicorn main:app --reload

5. Access the API:

       /metrics – http://localhost:8000/metrics?start=YYYY-MM-DD&end=YYYY-MM-DD
       /nl2sql – http://localhost:8000/nl2sql



## License
This project is licensed under the MIT License.

## Author
Zaiba Thabassum K – (https://github.com/zaibagithub)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) – For building the API  
- [OpenAI GPT-3.5](https://openai.com/) – For natural language to SQL  
- [n8n](https://n8n.io/) – Workflow automation
  

Explore, use, and improve! Your feedback is highly appreciated.


 
  

