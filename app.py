import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SolarCast", layout="wide")
st.title("SolarCast — Prévision de production photovoltaïque")

df = pd.read_csv("data/predictions.csv", index_col=0, parse_dates=True)

# Métriques
rmse = ((df["reel"] - df["predit"]) ** 2).mean() ** 0.5
rmse_p = ((df["reel"] - df["persistance"]) ** 2).mean() ** 0.5
mae = (df["reel"] - df["predit"]).abs().mean()

c1, c2, c3 = st.columns(3)
c1.metric("RMSE", f"{rmse:.0f} kW")
c2.metric("MAE", f"{mae:.0f} kW")
c3.metric("Skill score", f"{100*(1-rmse/rmse_p):.1f} %")

# Sélection de la journée
jours = sorted(set(df.index.date))
jour = st.selectbox("Journée", jours)

sel = df[df.index.date == jour]

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(sel.index, sel["reel"], label="Réel", linewidth=2)
ax.plot(sel.index, sel["predit"], label="Prévision 1 h", linewidth=2)
ax.set_ylabel("Puissance AC (kW)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.caption("Modèle : Random Forest — météo Open-Meteo (réanalyse ERA5) et état récent de la centrale")