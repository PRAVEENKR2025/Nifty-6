from fastapi import APIRouter, HTTPException
import os

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

# Company tearsheet PDF
@router.get("/company/{ticker}")
def company_report(ticker: str):
    path = f"reports/company_{ticker}.pdf"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Company report not found")
    return {"report_path": path}

# Portfolio report PDF
@router.get("/portfolio/{portfolio_id}")
def portfolio_report(portfolio_id: int):
    path = f"reports/portfolio_{portfolio_id}.pdf"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Portfolio report not found")
    return {"report_path": path}

# Analytics summary PDF
@router.get("/analytics")
def analytics_report():
    path = "reports/analytics_summary.pdf"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Analytics report not found")
    return {"report_path": path}
