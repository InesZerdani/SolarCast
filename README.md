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

**Erreur d'échelle détectée dans le dataset.** Le calcul du rendement de
conversion des onduleurs donnait 9,8 %, valeur physiquement impossible.
La puissance DC était surévaluée d'un facteur 10 ; après correction, le
rendement s'établit à 97,7 %.

**Distinction nowcasting / prévision.** Les premiers modèles atteignaient
80 % de skill score, mais utilisaient l'irradiance mesurée au même
instant — information indisponible en situation réelle. Sans elle, la
prévision à 1 h atteint 30,5 % de skill score, grâce au profil horaire et
à l'état récent de la centrale.

**Apport limité de la météo.** L'ajout des données ERA5 n'améliore pas la
prévision (3898 kW contre 3930 kW sans météo) : la maille de la réanalyse
est trop grossière pour capter les nuages au-dessus du site.

**Décalage temporel corrigé.** Les nuits ayant été retirées, un décalage
en nombre de pas (`shift`) sautait d'un jour à l'autre. Les cibles et la
production de la veille sont calculées par décalage exact en temps.

**Non-linéarité de la relation irradiance-production.** La production
s'infléchit au-delà de 0,8 d'irradiance, cohérent avec les pertes
thermiques des modules (-0,4 %/°C) et un écrêtage onduleur.

## Dashboard

    pip install -r requirements.txt
    streamlit run app.py

## Suite

Optimisation du pilotage d'une batterie de stockage à partir des prévisions.

## Outils

Python, pandas, NumPy, scikit-learn, XGBoost, pvlib, Streamlit,
matplotlib, seaborn

## Auteur

Ines Zerdani — MSc Intelligence Artificielle