import streamlit as st
import numpy as np
from strategies.strategy_database import STRATEGY_DATABASE
from core.financial_calcs import calculate_payoff_at_expiration
from core.plotting import create_pnl_chart

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Kriterion Options Playbook",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Kriterion Options Playbook")
st.markdown("Il simulatore interattivo per strategie in opzioni.")

# --- Sidebar per Input Utente ---
st.sidebar.header("Parametri di Input")

selected_strategy_name = st.sidebar.selectbox(
    "1. Scegli una Strategia",
    options=list(STRATEGY_DATABASE.keys())
)

strategy_details = STRATEGY_DATABASE[selected_strategy_name]
st.sidebar.info(strategy_details["description"])

center_strike = st.sidebar.number_input(
    "2. Strike Centrale (K)",
    value=100.0,
    step=0.5
)

underlying_price = st.sidebar.number_input(
    "3. Prezzo Sottostante (S)",
    value=100.0,
    step=0.5
)

# --- Area Principale per il Grafico ---
if selected_strategy_name:
    
    # 1. Definisci il range di prezzi da analizzare
    price_range = np.linspace(underlying_price * 0.7, underlying_price * 1.3, 200)

    # 2. Calcola il payoff
    payoff_values = calculate_payoff_at_expiration(
        strategy_legs=strategy_details["legs"],
        center_strike=center_strike,
        underlying_range=price_range
    )

    # 3. Crea il grafico
    pnl_chart = create_pnl_chart(
        underlying_range=price_range,
        payoff=payoff_values,
        strategy_name=selected_strategy_name
    )

    # 4. Mostra il grafico
    st.plotly_chart(pnl_chart, use_container_width=True)

else:
    st.info("Seleziona una strategia dalla barra laterale per iniziare.")
