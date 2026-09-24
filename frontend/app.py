import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns


API_URL = "http://127.0.0.1:8000/api/v1"
if "token" not in st.session_state:
    st.session_state.token = None

st.set_page_config(page_title="N100 Dashboard", layout="wide")

st.title("📊 N100 Financial Intelligence Dashboard")

# Health check
if st.button("Check API Health"):
    resp = requests.get(f"{API_URL}/health")
    st.json(resp.json())

# Companies
st.header("🏢 Companies")
sector = st.text_input("Filter by sector")
search = st.text_input("Search company name")
if st.button("List Companies"):
    params = {}
    if sector:
        params["sector"] = sector
    if search:
        params["search"] = search
    resp = requests.get(f"{API_URL}/companies/", params=params)
    st.json(resp.json())

ticker = st.text_input("Enter Ticker for Profile")
if st.button("Get Company Profile"):
    resp = requests.get(f"{API_URL}/companies/{ticker}")
    st.json(resp.json())

# Financials
st.header("💰 Financials")
fticker = st.text_input("Ticker for Financial Data")
if st.button("P&L"):
    st.json(requests.get(f"{API_URL}/financials/pl/{fticker}").json())
if st.button("Balance Sheet"):
    st.json(requests.get(f"{API_URL}/financials/balance/{fticker}").json())
if st.button("Cashflow"):
    st.json(requests.get(f"{API_URL}/financials/cashflow/{fticker}").json())
if st.button("Ratios"):
    st.json(requests.get(f"{API_URL}/financials/ratios/{fticker}").json())
if st.button("Tearsheet"):
    st.json(requests.get(f"{API_URL}/financials/tearsheet/{fticker}").json())

# Screener
st.header("🔍 Screener")
min_roe = st.number_input("Min ROE %", value=0.0)
max_de = st.number_input("Max Debt/Equity", value=10.0)
if st.button("Run Screener"):
    params = {"min_roe": min_roe, "max_debt_to_equity": max_de}
    resp = requests.get(f"{API_URL}/screener/", params=params)
    st.json(resp.json())

# Portfolio
st.header("📂 Portfolio")
p_id = st.number_input("Portfolio ID", value=1)
if st.button("List Portfolios"):
    st.json(requests.get(f"{API_URL}/portfolio/").json())
if st.button("Get Portfolio"):
    st.json(requests.get(f"{API_URL}/portfolio/{p_id}").json())
if st.button("List Holdings"):
    st.json(requests.get(f"{API_URL}/portfolio/{p_id}/holdings").json())

# Analytics
st.header("📈 Analytics")
if st.button("Cluster Profiles"):
    st.json(requests.get(f"{API_URL}/analytics/clusters").json())
if st.button("Outlier Report"):
    st.json(requests.get(f"{API_URL}/analytics/outliers").json())
if st.button("Portfolio Stats"):
    st.json(requests.get(f"{API_URL}/analytics/stats").json())



# Visualization: Ratios chart
st.header("📊 Ratio Visualization")
rticker = st.text_input("Ticker for Ratio Chart")
if st.button("Show Ratios Chart"):
    resp = requests.get(f"{API_URL}/financials/ratios/{rticker}")
    data = resp.json()
    if data:
        df = pd.DataFrame([data])
        st.bar_chart(df.T)

# Visualization: Growth trend
st.header("📈 Growth Trend")
gticker = st.text_input("Ticker for Growth Trend")
if st.button("Show Growth Trend"):
    resp = requests.get(f"{API_URL}/financials/pl/{gticker}")
    data = resp.json()
    if data:
        df = pd.DataFrame(data)
        fig, ax = plt.subplots()
        ax.plot(df["year"], df["revenue"], marker="o", label="Revenue")
        ax.plot(df["year"], df["net_income"], marker="o", label="Net Income")
        ax.set_title(f"{gticker} Growth Trend")
        ax.legend()
        st.pyplot(fig)

# Visualization: Cluster heatmap
st.header("🔬 Cluster Heatmap")
if st.button("Show Correlation Heatmap"):
    path = f"{API_URL}/analytics/correlation"
    resp = requests.get(path).json()
    heatmap_path = resp.get("heatmap_path")
    if heatmap_path and os.path.exists(heatmap_path):
        st.image(heatmap_path, caption="Correlation Heatmap")


st.sidebar.title("🔐 Authentication")

choice = st.sidebar.radio("Select Action", ["Signup", "Login", "Profile"])

if choice == "Signup":
    st.sidebar.subheader("Create Account")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Signup"):
        resp = requests.post(f"{API_URL}/auth/signup", params={"username": username, "password": password})
        st.sidebar.json(resp.json())

elif choice == "Login":
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        resp = requests.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
        if resp.status_code == 200:
            st.session_state.token = resp.json()["access_token"]
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid credentials")

elif choice == "Profile":
    st.sidebar.subheader("Profile Info")
    if st.session_state.token:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        resp = requests.get(f"{API_URL}/auth/me", headers=headers)
        st.sidebar.json(resp.json())
    else:
        st.sidebar.warning("Please login first")
