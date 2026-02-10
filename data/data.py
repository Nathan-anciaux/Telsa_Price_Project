import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# =====================================================
# Data
# =====================================================

path = "./data"
file = "tesla_stock_data_2010_2025.csv"
df = pd.read_csv(f"{path}/{file}")
