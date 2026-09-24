import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Step 1: Load data and cluster labels
df = pd.read_csv("data/companies.csv")
clusters = pd.read_csv("output/cluster_labels.csv")
df = df.merge(clusters, on="company_id")

# Step 2: Profile each cluster (mean & median of features)
features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct"
]

cluster_profile = df.groupby("cluster_id")[features].agg(["mean", "median"])
cluster_profile.to_csv("output/cluster_profiles.csv")

# Step 3: Assign descriptive names (example mapping)
cluster_names = {
    0: "High-Quality Compounders",
    1: "Defensive Dividend Payers",
    2: "Value Cyclicals",
    3: "Distressed or Turnaround",
    4: "Emerging Growth"
}
df["cluster_name"] = df["cluster_id"].map(cluster_names)

# Step 4: Correlation heatmap (10 KPIs)
kpi_cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct"
    # Add other KPIs if available
]
corr = df[kpi_cols].corr(method="pearson")

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap of KPIs")
plt.savefig("reports/correlation_heatmap.png")
plt.close()

# Step 5: Outlier detection (Z-score > 3 per sector)
outliers = []
for sector, group in df.groupby("broad_sector"):
    zscores = group[features].apply(zscore)
    mask = (zscores.abs() > 3).any(axis=1)
    flagged = group.loc[mask, ["company_id", "company_name", "broad_sector"]]
    outliers.append(flagged)

outlier_report = pd.concat(outliers)
outlier_report.to_csv("output/outlier_report.csv", index=False)

# Step 6: Portfolio statistics (percentiles + mean/std)
stats = df[features].describe(percentiles=[0.1,0.25,0.5,0.75,0.9]).T
stats.to_csv("output/portfolio_stats.csv")
