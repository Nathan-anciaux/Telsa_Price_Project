import pandas as pd
# j'importe RandomForest de sklearn
from sklearn.ensemble import RandomForestRegressor

# =====================================================
# DataManager
# =====================================================
"""
# j'importe les données de tesla que je mets dans une variable
path = "./data"
file = "tesla_stock_data_2010_2025.csv"
jeux_tesla = pd.read_csv(f"{path}/{file}")

#on supprime les endroits vides
jeux_tesla = jeux_tesla.dropna()


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


# j'importe chaque colonne du jeu de test
Column_tesla = ["Open", "High", "Low", "Volume", "MA_7", "Volatility_7d"]
X = jeux_tesla[Column_tesla]
y = jeux_tesla["Price_Range"]

model1 = RandomForestRegressor(
    n_estimators = 200,
    random_state = 42
)
model1.fit(X , y)

default_values = X.mean().to_dict()
"""

class DataManager:
    # chargen nettoie et prédis avec les données qu'on a transmis
    def __init__(self):
        path = "./data"
        file = "tesla_stock_data_2010_2025.csv"

        # on charge le CSV et on retire les ligne vide direct
        self.jeux_tesla = pd.read_csv(f"{path}/{file}").dropna()
        self._feature_names = ["Open", "High", "Low", "Volume", "MA_7", "Volatility_7d"]

        # data = colonnes d'entrées
        # target la valeur qu'on veut prédire
        self._data = self.jeux_tesla[self._feature_names]
        self._target = self.jeux_tesla["Price_Range"]
        self._target_names = "Price_Range"

        self._model = RandomForestRegressor(
            n_estimators = 200,
            random_state = 42
        )
        self._model.fit(self._data, self._target)

        # on calcule la moyenne de chaque colonne pour initialiser l'application
        self.default_values = self._data.mean().to_dict()

    def get_data(self):
        return self._data
    
    def get_target(self):
        return self._target
    
    def get_target_names(self):
        return self._target_names
    
    def get_features_names(self):
        return self._feature_names
    
    def get_model_prediction(self, x_values):
        # on convertit le dictionnaire en liste dans le bon ordre 
        if isinstance(x_values, dict):
            x_values = [x_values[feature] for feature in self._feature_names]

        # convertion en DataFrame pour sklearn soit ok avec
        X_input = pd.DataFrame([x_values], columns=self._feature_names)

        # retourne la valeur prédite
        return self._model.predict(X_input)[0]
    
    def get_default_feature(self):
        # colonne affiché au lancement du site
        return "Open"
    
    def get_default_values(self):
        return self.default_values
    
    def get_full_dataframe(self):
        return self.jeux_tesla

    def get_defaults(self):
        # pratique pour initialiser le dcc.store de dash
       return self.get_default_values()