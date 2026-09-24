from fastapi import APIRouter, Query
import sqlite3

router = APIRouter(prefix="/api/v1/screener", tags=["screener"])

def get_db_connection():
    conn = sqlite3.connect("data/n100.db")
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
def screen_companies(
    min_roe: float = Query(None, description="Minimum Return on Equity %"),
    max_debt_to_equity: float = Query(None, description="Maximum Debt to Equity"),
    min_revenue_cagr: float = Query(None, description="Minimum 5yr Revenue CAGR %"),
    min_fcf_cagr: float = Query(None, description="Minimum 5yr FCF CAGR %"),
    min_op_margin: float = Query(None, description="Minimum Operating Profit Margin %"),
    sector: str = Query(None, description="Filter by broad sector")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT company_id, company_name, broad_sector, roe_pct, debt_to_equity, revenue_cagr_5yr, fcf_cagr_5yr, operating_profit_margin_pct FROM companies"
    filters = []
    params = []

    if min_roe is not None:
        filters.append("roe_pct >= ?")
        params.append(min_roe)
    if max_debt_to_equity is not None:
        filters.append("debt_to_equity <= ?")
        params.append(max_debt_to_equity)
    if min_revenue_cagr is not None:
        filters.append("revenue_cagr_5yr >= ?")
        params.append(min_revenue_cagr)
    if min_fcf_cagr is not None:
        filters.append("fcf_cagr_5yr >= ?")
        params.append(min_fcf_cagr)
    if min_op_margin is not None:
        filters.append("operating_profit_margin_pct >= ?")
        params.append(min_op_margin)
    if sector is not None:
        filters.append("broad_sector = ?")
        params.append(sector)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
