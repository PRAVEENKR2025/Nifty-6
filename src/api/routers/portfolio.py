from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])

def get_db_connection():
    conn = sqlite3.connect("data/n100.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create a new portfolio
@router.post("/")
def create_portfolio(name: str, owner: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO portfolios (name, owner) VALUES (?, ?)", (name, owner))
    conn.commit()
    portfolio_id = cursor.lastrowid
    conn.close()
    return {"portfolio_id": portfolio_id, "name": name, "owner": owner}

# List all portfolios
@router.get("/")
def list_portfolios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolios")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Get portfolio details
@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolios WHERE portfolio_id = ?", (portfolio_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return dict(row)

# Add a holding to portfolio
@router.post("/{portfolio_id}/holdings")
def add_holding(portfolio_id: int, ticker: str, shares: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO holdings (portfolio_id, ticker, shares) VALUES (?, ?, ?)",
        (portfolio_id, ticker, shares)
    )
    conn.commit()
    conn.close()
    return {"portfolio_id": portfolio_id, "ticker": ticker, "shares": shares}

# List holdings in a portfolio
@router.get("/{portfolio_id}/holdings")
def list_holdings(portfolio_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM holdings WHERE portfolio_id = ?", (portfolio_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Delete a portfolio
@router.delete("/{portfolio_id}")
def delete_portfolio(portfolio_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM portfolios WHERE portfolio_id = ?", (portfolio_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "portfolio_id": portfolio_id}
