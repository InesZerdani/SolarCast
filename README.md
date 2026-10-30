# SolarCast

Prévision de production photovoltaïque par apprentissage automatique, à
partir de données météorologiques et de l'état récent de la centrale.

## Problème

Un gestionnaire de centrale doit annoncer à l'avance la puissance qu'il
injectera sur le réseau. Cette prévision dépend de la météo future, et non
de mesures disponibles seulement a posteriori.

## Données

- Production d'une centrale photovoltaïque indienne (34 jours, pas de
  15 minutes, 22 onduleurs) — [dataset public Kaggle](https://www.kaggle.com/datasets/anikannal/solar-power-generation-data)
- Données météorologiques Open-Meteo (réanalyse ERA5) : rayonnement
  global, direct et diffus, couverture nuageuse à trois altitudes,
  température, humidité, vent, précipitations

## Résultats

Prévision à 1 heure, séparation temporelle 80/20 :

| Modèle | RMSE (kW) | Skill score |
|---|---|---|
| Persistance (référence) | 5581 | 0 % |
| XGBoost | 4003 | 28,3 % |
| **Random Forest** | **3898** | **30,2 %** |

Performance selon l'horizon de prévision :

| Horizon | 15 min | 30 min | 1 h | 2 h | 3 h | 6 h |
|---|---|---|---|---|---|---|
| Skill score | 4,4 % | 15,8 % | 30,1 % | 50,5 % | 58,7 % | 69,0 % |

Le gain augmente avec l'horizon : la persistance se dégrade rapidement,
tandis que le modèle reste stable autour de 4000 kW de RMSE.

## Démarche

| Notebook | Contenu |
|---|---|
| `01_exploration.ipynb` | Chargement, visualisations, détection d'anomalies |
| `02_nettoyage.ipynb` | Horodatages manquants, interpolation, filtrage des heures de nuit |
| `03_exploration.ipynb` | Profils horaires, corrélations |
| `04_features.ipynb` | Encodage cyclique, position solaire (pvlib), variables retardées |
| `05_models.ipynb` | Premiers modèles — mise en évidence d'un problème de nowcasting |
| `06_meteo_prevision.ipynb` | Prévision avec données météo, comparaison des horizons |

## Points notables

## Points notables

- Erreur d'échelle ×10 sur la puissance DC, détectée par le rendement onduleur
- Premiers modèles en nowcasting (80 %), reformulés en vraie prévision (30 % à 1 h)
- La météo ERA5 n'améliore pas la prévision : maille trop grossière
- Décalages temporels recalculés en temps exact (les nuits étant retirées)

Détails des anomalies, erreurs et décisions : [docs/analyse.md](docs/analyse.md)

## Dashboard

    pip install -r requirements.txt
    streamlit run app.py

## Suite

Optimisation du pilotage d'une batterie de stockage à partir des prévisions.

## Outils

Python, pandas, NumPy, scikit-learn, XGBoost, pvlib, Streamlit,
matplotlib, seaborn

