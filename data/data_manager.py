import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from configparser import ConfigParser

# =====================================================
# DataManager
# =====================================================


class DataManager:
    def __init__(self, config_file="config.ini"):
        self.config = ConfigParser(interpolation=None)
        self.config.read(config_file)

        self.liste_marques = [
            n.strip()
            for n in self.config.get("GENERAL", "datasets_a_charger").split(",")
        ]
        self.infos_marques = {}  # Stockera couleurs, logos, etc.

        self.dataframes = {}  # données brut
        self.features_dict = {}  # colonnes select
        self.features_ia_dict = {}  # colonnes used by the ai
        self.target_names = {}  # name de la var a prédire
        self.models = {}  # Randomforest entrainés
        self.default_values_dict = {}  # pour remplir par defaut par moyenne

        # On lit la liste des datasets a charger
        datasets_bruts = self.config.get("GENERAL", "datasets_a_charger")
        liste_datasets = [nom.strip() for nom in datasets_bruts.split(",")]

        for nom_dataset in liste_datasets:
            self._charger_un_dataset(nom_dataset)

        for nom in self.liste_marques:
            self._charger_un_dataset(nom)
            # On récupère les infos visuelles
            self.infos_marques[nom] = {
                "couleur": self.config.get(nom, "couleur", fallback="#ffffff"),
                "logo": self.config.get(nom, "logo", fallback=""),
                "description": self.config.get(nom, "description", fallback=""),
            }

    def get_marques(self):
        return self.liste_marques

    def get_info(self, marque, cle):
        return self.infos_marques.get(marque, {}).get(cle)

    def _charger_un_dataset(self, nom_dataset):
        # parametre de config
        chemin = self.config.get(nom_dataset, "chemin")
        features_brutes = self.config.get(nom_dataset, "features")
        target_name = self.config.get(nom_dataset, "target")
        features_ui = [f.strip() for f in features_brutes.split(",")]

        df = pd.read_csv(chemin)

        # nettoyage
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        colonnes_a_nettoyer = list(set(features_ui + [target_name, "High", "Low"]))

        for col in colonnes_a_nettoyer:
            if col in df.columns:
                # on supprime les $ et convertir en nombre
                df[col] = df[col].astype(str).str.replace("$", "", regex=False)
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # calcul la volatilité
        if "Price_Range" not in df.columns:
            if "High" in df.columns and "Low" in df.columns:
                df["Price_Range"] = df["High"] - df["Low"]
            else:
                raise ValueError(
                    f"Les colonnes High et Low sont absentes dans {nom_dataset}."
                )

        # la cible (volatility en pourcentage)
        df["Volatilite_Pourcentage"] = ((df["High"] - df["Low"]) / df["Open"]) * 100
        target_name = "Volatilite_Pourcentage"

        # on prépare  l'ia en exluant les données futurs
        colonnes_interdites = ["High", "Low", "Close"]
        features_ia = [col for col in features_ui if col not in colonnes_interdites]

        # entraine le model
        colonnes_model = features_ia + [target_name]
        df_ml = df[colonnes_model].dropna()

        X = df_ml[features_ia]
        y = df_ml[target_name]
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # on sauvegarde les résultats
        self.dataframes[nom_dataset] = df
        self.features_dict[nom_dataset] = features_ui
        self.features_ia_dict[nom_dataset] = features_ia
        self.target_names[nom_dataset] = target_name
        self.models[nom_dataset] = model
        self.default_values_dict[nom_dataset] = df[features_ui].mean().to_dict()

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
        """réalise la prédiction avec les paramètres en question"""
        features_ia = self.features_ia_dict[nom_dataset]
        model = self.models[nom_dataset]

        if isinstance(x_values, dict):
            x_values = [x_values[feature] for feature in features_ia]

        X_input = pd.DataFrame([x_values], columns=features_ia)
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
        # on découpe une colonnes en 4 quartiles
        df = self.dataframes[nom_dataset]

        return pd.cut(
            df[column_name],
            bins=4,
            labels=[
                "Quartile 1 (Low)",
                "Quartile 2",
                "Quartile 3",
                "Quartile 4 (High)",
            ],
        )

    def get_pie_chart_data(self, nom_dataset, feature):
        # retourne les index et val du graphique
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
        # on recupere toutes les caractéristiques d'un dataset pour une date précise
        df = self.dataframes[nom_dataset]
        features = self.features_dict[nom_dataset]

        ligne = df[df["Date"] == date_string]

        if ligne.empty:
            return None

        features_dict = {}
        for col in features:
            features_dict[col] = float(ligne[col].values[0])

        return features_dict
    
    def get_chart_indicators(self, active_brand):
        # Analyse les données et retourne un dictionnaire des lignes à tracer
        df = self.get_full_dataframe(active_brand)
        indicators = {}
        
        for col in df.columns:
            if col.startswith("MA_"):
                jours = col.split("_")[1]
                indicators[col] = f"Moyenne {jours}j"
                
        return indicators
    
