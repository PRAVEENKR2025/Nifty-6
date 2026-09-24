from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(prefix="/api/v1/financials", tags=["financials"])

def get_db_connection():
    conn = sqlite3.connect("data/n100.db")
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/pl/{ticker}")
def profit_and_loss(ticker: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profit_loss WHERE ticker = ?", (ticker,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="P&L not found")
    return [dict(row) for row in rows]

@router.get("/balance/{ticker}")
def balance_sheet(ticker: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balance_sheet WHERE ticker = ?", (ticker,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Balance sheet not found")
    return [dict(row) for row in rows]

@router.get("/cashflow/{ticker}")
def cashflow(ticker: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cashflow WHERE ticker = ?", (ticker,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Cashflow not found")
    return [dict(row) for row in rows]

@router.get("/ratios/{ticker}")
def ratios(ticker: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financial_ratios WHERE ticker = ?", (ticker,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Ratios not found")
    return [dict(row) for row in rows]

@router.get("/tearsheet/{ticker}")
def tearsheet(ticker: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tearsheets WHERE ticker = ?", (ticker,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Tearsheet not found")
    return dict(row)
