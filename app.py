import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="CO2 Flare Supervision System", layout="wide")

st.title("🔥 Système intelligent de gestion du CO₂ (Torchère / Récupération)")
st.markdown("Simulation d’un système industriel inspiré de Sonatrach")

# =========================
# Initialisation mémoire
# =========================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Cycle", "CO2 (%)", "Débit", "Décision"]
    )

# =========================
# Bouton RUN
# =========================
run = st.button("▶ RUN SYSTEM")

if run:
    cycle = len(st.session_state.data) + 1

    co2 = random.uniform(30, 70)
    debit = random.uniform(1000, 6000)

    if co2 >= 50 or debit > 5000:
        decision = "TORCHÈRE"
    else:
        decision = "RÉCUPÉRATION"

    new_row = {
        "Cycle": cycle,
        "CO2 (%)": round(co2, 2),
        "Débit": int(debit),
        "Décision": decision
    }

    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )

# =========================
# Affichage dernière lecture
# =========================
if not st.session_state.data.empty:
    last = st.session_state.data.iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("CO₂ (%)", last["CO2 (%)"])
    col2.metric("Débit (m³/h)", last["Débit"])
    
    if last["Décision"] == "TORCHÈRE":
        col3.error("🔥 TORCHÈRE")
    else:
        col3.success("✅ RÉCUPÉRATION")

# =========================
# Graphique CO2
# =========================
st.subheader("📈 Évolution du CO₂")

if not st.session_state.data.empty:
    st.line_chart(st.session_state.data.set_index("Cycle")["CO2 (%)"])

# =========================
# Historique
# =========================
st.subheader("📋 Historique des décisions")
st.dataframe(st.session_state.data)
