import streamlit as st
import numpy as np
from strategies.strategy_database import STRATEGY_DATABASE
from core.financial_calcs import calculate_pnl_and_greeks
from core.plotting import create_pnl_chart

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Kriterion Options Playbook",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Kriterion Options Playbook")
st.markdown("Il simulatore interattivo per strategie in opzioni - **Fase 2: Analisi Avanzata**")

# --- Sidebar per Input Utente ---
st.sidebar.header("Parametri di Input")

# 1. Scelta Strategia
selected_strategy_name = st.sidebar.selectbox(
    "1. Scegli una Strategia",
    options=list(STRATEGY_DATABASE.keys())
)
strategy_details = STRATEGY_DATABASE[selected_strategy_name]
st.sidebar.info(strategy_details["description"])

# 2. Parametri di Mercato e Contratto
st.sidebar.subheader("2. Parametri di Mercato")
underlying_price = st.sidebar.number_input("Prezzo Sottostante (S)", value=100.0, step=0.5)
center_strike = st.sidebar.number_input("Strike Centrale (K)", value=100.0, step=0.5)

# 3. Parametri per Analisi Avanzata
st.sidebar.subheader("3. Parametri di Analisi")
days_to_expiration = st.sidebar.slider(
    "Giorni alla Scadenza (DTE)", 
    min_value=1, max_value=365, value=30
)
implied_volatility = st.sidebar.slider(
    "Volatilità Implicita (%)", 
    min_value=5, max_value=150, value=20
)

# --- Area Principale ---
if selected_strategy_name:
    
    # 1. Definisci il range di prezzi
    price_range = np.linspace(underlying_price * 0.7, underlying_price * 1.3, 200)

    # 2. Calcola P/L e Greche
    pnl_T, pnl_exp, greeks = calculate_pnl_and_greeks(
        strategy_legs=strategy_details["legs"],
        center_strike=center_strike,
        underlying_range=price_range,
        days_to_expiration=days_to_expiration,
        implied_volatility=implied_volatility
    )

    # 3. Mostra la Dashboard delle Greche 
    st.subheader("Dashboard delle Greche Aggregate")
    cols = st.columns(4)
    cols[0].metric("Delta", f"{greeks['delta']:.4f}")
    cols[1].metric("Gamma", f"{greeks['gamma']:.4f}")
    cols[2].metric("Theta", f"{greeks['theta']:.4f}")
    cols[3].metric("Vega", f"{greeks['vega']:.4f}")
    
    st.markdown("---")

    # 4. Crea e mostra il grafico
    st.subheader("Grafico Profit/Loss")
    pnl_chart = create_pnl_chart(
        underlying_range=price_range,
        pnl_at_T=pnl_T,
        pnl_at_expiration=pnl_exp,
        strategy_name=selected_strategy_name,
        days_to_expiration=days_to_expiration
    )
    st.plotly_chart(pnl_chart, use_container_width=True)

else:
    st.info("Seleziona una strategia dalla barra laterale per iniziare.")
