# SolarCast

Prévision de production photovoltaïque par apprentissage automatique, à
partir de prévisions météorologiques et de l'état récent de la centrale.

## Problème

Un gestionnaire de centrale doit annoncer à l'avance la puissance qu'il
injectera sur le réseau. Cette prévision dépend de la météo future, et non
de mesures disponibles seulement a posteriori.

## Données

- Production d'une centrale photovoltaïque indienne (34 jours, pas de
  15 minutes, 22 onduleurs) — dataset public Kaggle
- Prévisions météorologiques Open-Meteo (archives ERA5) : rayonnement
  global, direct et diffus, couverture nuageuse à trois altitudes,
  température, humidité, vent, précipitations

## Résultats

Prévision à 1 heure, Random Forest, séparation temporelle 80/20 :

| Modèle | RMSE (kW) | Skill score |
|---|---|---|
| Persistance (référence) | 5380 | 0 % |
| XGBoost | 3935 | 26,9 % |
| **Random Forest** | **3712** | **31,0 %** |

Performance selon l'horizon de prévision :

| Horizon | 15 min | 30 min | 1 h | 2 h | 3 h | 6 h |
|---|---|---|---|---|---|---|
| Skill score | 3,8 % | 15,4 % | 30,9 % | 51,4 % | 60,5 % | 68,9 % |

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
| `06_meteo_prevision.ipynb` | Passage à la prévision réelle avec données météo |

## Points notables

**Erreur d'échelle détectée dans le dataset.** Le calcul du rendement de
conversion des onduleurs donnait 9,8 %, valeur physiquement impossible.
La puissance DC était surévaluée d'un facteur 10 ; après correction, le
rendement s'établit à 97,7 %.

**Distinction nowcasting / prévision.** Les premiers modèles atteignaient
80 % de skill score, mais utilisaient l'irradiance mesurée au même
instant — information indisponible en situation réelle. Privés de cette
variable, ils faisaient moins bien que la persistance. Le problème a été
reformulé avec des prévisions météorologiques, seules données réellement
disponibles à l'avance.

**Non-linéarité de la relation irradiance-production.** La production
s'infléchit au-delà de 0,8 d'irradiance, cohérent avec les pertes
thermiques des modules (-0,4 %/°C) et un écrêtage onduleur.

## Dashboard
Lancer le dashboard :

    streamlit run app.py

Nécessite d'avoir exécuté les notebooks au préalable pour générer
`data/predictions.csv`.

## Outils

Python, pandas, NumPy, scikit-learn, XGBoost, pvlib, Streamlit,
matplotlib, seaborn

## Auteur

Ines Zerdani — MSc Intelligence Artificielle