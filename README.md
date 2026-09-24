# 📊 N100 Financial Intelligence API

## Overview
N100 is a FastAPI + Streamlit project for financial analytics on Nifty-100 companies.  
It provides endpoints for companies, financials, portfolios, analytics, and reports, with role-based authentication.

## Features
- FastAPI backend with Swagger docs
- Streamlit frontend dashboard
- Companies, financials, screener, portfolio, analytics endpoints
- Reports generation (PDFs)
- Authentication + RBAC (admin, analyst, viewer)

## Installation
```bash
git clone <repo-url>
cd nifty-6
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
