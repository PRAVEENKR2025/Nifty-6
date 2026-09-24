from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

# Cluster profiles
@router.get("/clusters")
def get_cluster_profiles():
    path = "output/cluster_profiles.csv"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Cluster profiles not found")
    df = pd.read_csv(path)
    return df.to_dict(orient="records")

# Correlation heatmap (return as file path)
@router.get("/correlation")
def get_correlation_heatmap():
    path = "reports/correlation_heatmap.png"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Correlation heatmap not found")
    return {"heatmap_path": path}

# Outlier report
@router.get("/outliers")
def get_outlier_report():
    path = "output/outlier_report.csv"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Outlier report not found")
    df = pd.read_csv(path)
    return df.to_dict(orient="records")

# Portfolio statistics
@router.get("/stats")
def get_portfolio_stats():
    path = "output/portfolio_stats.csv"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Portfolio stats not found")
    df = pd.read_csv(path)
    return df.to_dict(orient="records")
