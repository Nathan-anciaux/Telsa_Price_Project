import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# =====================================================
# DATA
# =====================================================
path = "./"
file = "tesla_stock_data_2010_2025.csv" 
df = pd.read_csv(f"{path}/{file}")

df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# =====================================================

df['MA7'] = df['Close'].rolling(window=7).mean()   
df['MA30'] = df['Close'].rolling(window=30).mean() 
df['Return'] = df['Close'].pct_change()            

# La cible (y) : on veut prédire le prix du LENDEMAIN
df['Target'] = df['Close'].shift(-1)

df = df.dropna()

feature_names = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA7', 'MA30', 'Return']
X = df[feature_names]
y = df['Target']

# =====================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

default_values = X.mean().to_dict()

print(f"Modèle entraîné. Score R² : {model.score(X_test, y_test):.4f}")