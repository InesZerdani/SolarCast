# SolarCast — Analyse détaillée

Anomalies rencontrées, erreurs corrigées et décisions prises, notebook par notebook.

## 1. Qualité des données (01)

**Puissance DC surévaluée ×10**
- Rendement onduleur apparent de 9,8 %, physiquement impossible
- Correction `DC_POWER / 10` → rendement de 97,7 %, conforme aux valeurs constructeur

**Ratios AC/DC > 100 %**
- 18 points sur 36 827, dont 16 au même instant (14/06, 8h30) sur 16 onduleurs
- Surviennent vers 500 kW : l'hypothèse du bruit à faible puissance est réfutée
- Cause probable : décalage de mesure DC/AC pendant un passage nuageux
- Négligeable, et `DC_POWER` n'est pas conservé

**Pannes d'onduleurs**
- 63 points à production nulle malgré une irradiance > 0,1
- 14/06 : 2 onduleurs à l'arrêt de 11h15 à 14h, irradiance normale → défaut d'équipement local
- 07/06 : 32 points répartis sur 6 onduleurs, cause non identifiée
- Décision : cible = production agrégée de la centrale, pas par onduleur

## 2. Nettoyage (02)

- 10 trous dans la série (de 30 min à 9 h) → grille régulière de 15 min
- Interpolation linéaire limitée à 1 h : défendable sur de courts trous, pas au-delà
- 79 valeurs manquantes restantes, éliminées par le filtre jour (environ 67 la nuit, 12 le jour, moins de 0,8 % des données)
- Filtre `IRRADIATION > 0,01` → 50,6 % des points conservés
- 2 points à production nulle en plein soleil exclus → 1650 lignes

## 3. Analyse exploratoire (03)

- Irradiance / production : corrélation de 0,991 sans la nuit → relation réelle
- Température ambiante : 0,72 → 0,53 sans la nuit (corrélation surtout due au cycle jour/nuit)
- Température module : colinéaire avec l'irradiance (0,92)
- Plafonnement vers 29 000 kW au-delà de 0,8 d'irradiance : pertes thermiques (modules à 55–65 °C) et écrêtage onduleur

## 4. Variables (04)

- Coordonnées du site non fournies : approximation à 22° N, 78° E
- **Erreur corrigée** : `shift(96)` ne vaut pas 24 h une fois les nuits retirées (écart réel de 1 j 11 h à 2 j 15 h) → recherche exacte à t − 24 h
- `jour_sin` / `jour_cos` retirés : un mois de données ne permet pas d'apprendre une saisonnalité
- Indice de ciel clair borné à 1,2 (11 points concernés)

## 5. Modélisation (05)

**Nowcasting déguisé en prévision**
- Régression linéaire : RMSE 614 kW, skill score de 80 % face à la persistance à 15 min
- `IRRADIATION`, mesurée au même instant, concentre 99 % de l'importance → le modèle estime l'instant présent, il ne prévoit pas

**Erreur d'évaluation corrigée**
- La prévision à 1 h était comparée à la persistance à 15 min, et `shift(-4)` sautait la nuit
- Après correction : RMSE 3930 kW contre 5652 kW pour la persistance à 1 h → skill score de 30,5 %

## 6. Prévision avec météo (06)

- Rayonnement ERA5 corrélé à 0,71 avec la production, contre 0,99 pour le capteur du site (maille de plusieurs dizaines de km)
- Prévision à 1 h : Random Forest à 3898 kW (30,2 %), XGBoost à 4003 kW (28,3 %), persistance à 5581 kW
- **La météo n'apporte presque rien** : 3898 kW avec, 3930 kW sans
- L'encodage horaire pèse plus de 80 % de l'importance : le modèle apprend surtout le profil journalier
- Prévision trop lisse : passages nuageux non anticipés, pics sous-estimés, creux surestimés

| Horizon | 15 min | 30 min | 1 h | 2 h | 3 h | 6 h |
|---|---|---|---|---|---|---|
| Persistance (kW) | 3059 | 4214 | 5581 | 8605 | 10913 | 13164 |
| Random Forest (kW) | 2925 | 3549 | 3902 | 4264 | 4510 | 4086 |
| Skill score | 4,4 % | 15,8