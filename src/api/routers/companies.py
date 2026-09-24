from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

def get_db_connection():
    conn = sqlite3.connect("data/n100.db")
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
def list_companies(sector: str = None, market_cap_category: str = None, search: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT company_id, company_name, broad_sector, sub_sector, roe_pct, roce_pct FROM companies"
    filters = []
    params = []

    if sector:
        filters.append("broad_sector = ?")
        params.append(sector)
    if market_cap_category:
        filters.append("market_cap_category = ?")
        params.append(market_cap_category)
    if search:
        filters.append("company_name LIKE ?")
        params.append(f"%{search}%")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/{ticker}")
def company_profile(ticker: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE ticker = ?", (ticker,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Company not found")
    return dict(row)
