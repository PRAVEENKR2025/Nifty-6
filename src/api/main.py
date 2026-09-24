from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import time

# Step 1: Create FastAPI app
app = FastAPI(title="N100 Financial Intelligence API", version="1.0.0")

# Step 2: Database connection
def get_db_connection():
    conn = sqlite3.connect("data/n100.db")
    conn.row_factory = sqlite3.Row
    return conn

# Step 3: Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 4: Request logging
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} completed in {duration:.3f}s")
    return response

# Step 5: Health endpoint
@app.get("/api/v1/health")
def health_check():
    conn = get_db_connection()
    cursor = conn.cursor()
    tables = ["companies"]  # add more tables later
    db_row_counts = {}
    for t in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            db_row_counts[t] = cursor.fetchone()[0]
        except Exception:
            db_row_counts[t] = "N/A"
    conn.close()
    return {
        "status": "ok",
        "db_row_counts": db_row_counts,
        "uptime_seconds": int(time.time() - start_time_global),
        "version": "1.0.0"
    }

# Global uptime tracker
start_time_global = time.time()

# Step 6: Import routers AFTER app is defined
from src.api.routers import companies
app.include_router(companies.router)

from src.api.routers import financials
app.include_router(financials.router)

from src.api.routers import screener
app.include_router(screener.router)

from src.api.routers import portfolio
app.include_router(portfolio.router)

from src.api.routers import analytics
app.include_router(analytics.router)

from src.api.routers import reports
app.include_router(reports.router)

from src.api.routers import auth
app.include_router(auth.router)
