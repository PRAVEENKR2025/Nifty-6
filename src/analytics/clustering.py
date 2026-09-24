import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Step 1: Load your company dataset (replace with actual path)
df = pd.read_csv("data/companies.csv")

# Step 2: Select features for clustering
features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "operating_profit_margin_pct"
]

X = df[features].copy()

# Step 3: Impute missing values with sector median
for col in features:
    df[col] = df.groupby("broad_sector")[col].transform(
        lambda x: x.fillna(x.median())
    )

# Step 4: Scale features (zero mean, unit variance)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# Step 5: Run KMeans with 5 clusters
kmeans = KMeans(n_clusters=5, random_state=42)
df["cluster_id"] = kmeans.fit_predict(X_scaled)

# Step 6: Save cluster labels with distance from centroid
distances = kmeans.transform(X_scaled).min(axis=1)
output = pd.DataFrame({
    "company_id": df["company_id"],
    "cluster_id": df["cluster_id"],
    "distance_from_centroid": distances
})

output.to_csv("output/cluster_labels.csv", index=False)

# Step 7: Generate elbow plot (k=2 to 10)
inertias = []
K = range(2, min(11, len(X_scaled)))
for k in K:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.plot(K, inertias, marker="o")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Plot")
plt.savefig("reports/elbow_plot.png")
plt.close()
