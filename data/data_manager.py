import pandas as pd
# j'importe RandomForest de sklearn
from sklearn.ensemble import RandomForestRegressor
from configparser import ConfigParser

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
    def __init__(self,config_file='config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

        # databases pour stocker les 4 dataframes
        self.dataframes = {}
        self.features_dict = {}
        self.target_names = {}
        self.models = {}
        self.default_values_dict = {}

        datasets_bruts = self.config.get('GENERAL', 'datasets_a_charger')
        liste_datasets = [nom.strip() for nom in datasets_bruts.split(',')]

        for nom_dataset in liste_datasets:
            self._charger_un_dataset(nom_dataset)

    def _charger_un_dataset(self, nom_dataset):
        chemin = self.config.get(nom_dataset, 'chemin')
        features_brutes = self.config.get(nom_dataset, 'features')
        target_name = self.config.get(nom_dataset, 'target')

        # Nettoyage des noms de colonnes
        features = [f.strip() for f in features_brutes.split(',')]

        df = pd.read_csv(chemin).dropna()

        # machine learning
        X = df[features]
        y = df[target_name]
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # dico
        self.dataframes[nom_dataset] = df
        self.features_dict[nom_dataset] = features
        self.target_names[nom_dataset] = target_name
        self.models[nom_dataset] = model
        self.default_values_dict[nom_dataset] = X.mean().to_dict()

    def get_data(self, nom_dataset):
        df = self.dataframes[nom_dataset]
        features = self.features_dict[nom_dataset]
        return df[features]
    
    def get_target(self, nom_dataset):
        df = self.dataframes[nom_dataset]
        target_name = self.target_names[nom_dataset]
        return df[target_name]
    
    def get_target_names(self, nom_dataset):
        return self.target_names[nom_dataset]
    
    def get_features_names(self, nom_dataset):
        return self.features_dict[nom_dataset]
    
    def get_model_prediction(self, nom_dataset, x_values):
       
        features = self.features_dict[nom_dataset]
        model = self.models[nom_dataset]

        if isinstance(x_values, dict):
            x_values = [x_values[feature] for feature in features]

        X_input = pd.DataFrame([x_values], columns=features)
        return model.predict(X_input)[0]
    
    def get_default_feature(self, nom_dataset):
        
        return self.features_dict[nom_dataset][0]
    
    def get_default_values(self, nom_dataset):
        return self.default_values_dict[nom_dataset]
    
    def get_full_dataframe(self, nom_dataset):
        return self.dataframes[nom_dataset]

    def get_defaults(self, nom_dataset):
       return self.get_default_values(nom_dataset)
    
    def _get_pie_categories(self, nom_dataset, column_name):
        df = self.dataframes[nom_dataset]
        
        return pd.cut(
            df[column_name], 
            bins=4, 
            labels=["Quartile 1 (Bas)", "Quartile 2", "Quartile 3", "Quartile 4 (Haut)"]
        )

    def get_pie_chart_data(self, nom_dataset, feature):
        categories = self._get_pie_categories(nom_dataset, feature)
        
        comptage = categories.value_counts()
        return comptage.index.tolist(), comptage.values.tolist()

    def get_pie_category_mean(self, nom_dataset, column_name, label_clique):
        df = self.dataframes[nom_dataset]
        categories = self._get_pie_categories(nom_dataset, column_name)
        
        jours = df[column_name][categories == label_clique]
        
        moyenne = jours.mean()
        if pd.isna(moyenne):
            return None
            
        return float(moyenne)
    
    def get_features_by_date(self, nom_dataset, date_string):
        df = self.dataframes[nom_dataset]
        features = self.features_dict[nom_dataset]

        ligne = df[df["Date"] == date_string]
        
        if ligne.empty:
            return None
            
        features_dict = {}
        for col in features:
            features_dict[col] = float(ligne[col].values[0])
            
        return features_dict
    