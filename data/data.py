import pandas as pd
# j'importe RandomForest de sklearn
from sklearn.ensemble import RandomForestClassifier

# =====================================================
# Data
# =====================================================

# j'importe les données de tesla que je mets dans une variable
path = "./data"
file = "tesla_stock_data_2010_2025.csv"
jeux_tesla = pd.read_csv(f"{path}/{file}")

#on supprime les endroits vides
jeux_tesla = jeux_tesla.dropna()

"""
Date = jeux_tesla.Date
Open = jeux_tesla.Open
High = jeux_tesla.High
Low = jeux_tesla.Low
Close = jeux_tesla.Close
Volume = jeux_tesla.Volume
Daily_Return = jeux_tesla.Daily_Return
Price_Range = jeux_tesla.Price_Range
Price_Change = jeux_tesla.Price_Change
Price_Change_Percent = jeux_tesla.Price_Change_Percent
MA_7 = jeux_tesla.MA_7
MA_30 = jeux_tesla.MA_30
MA_90 = jeux_tesla.MA_90
Volatility_7d = jeux_tesla.Volatility_7d
Year = jeux_tesla.Year
Month = jeux_tesla.Month
Day_of_Week = jeux_tesla.Day_of_Week
Quarter = jeux_tesla.Quarter
"""

# j'importe chaque colonne du jeu de test
Column_tesla = ["Open", "High", "Low", "Volume", "MA_7", "Volatility_7d"]
X = jeux_tesla[Column_tesla]
y = jeux_tesla["Price_Range"]

test1 = pd.DataFrame(X, columns = Date)
test1["Price_range"] = y

model1 = RandomForestRegressor(
    n_estimators = 200,
    random_state = 42
)
model1.fit(X , y)

default_values = X.mean().to_dict()