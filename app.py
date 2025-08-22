import streamlit as st
import numpy as np
import pandas as pd
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
st.markdown("Il simulatore interattivo per strategie in opzioni.")

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

# --- Creazione Tab ---
tab1, tab2 = st.tabs(["Analisi Strategia", "Playbook (What-If)"])

# --- Contenuto Tab 1: Analisi Strategia ---
with tab1:
    if selected_strategy_name:
        # Calcola P/L e Greche
        price_range = np.linspace(underlying_price * 0.7, underlying_price * 1.3, 200)
        pnl_T, pnl_exp, greeks = calculate_pnl_and_greeks(
            strategy_legs=strategy_details["legs"],
            center_strike=center_strike,
            underlying_range=price_range,
            days_to_expiration=days_to_expiration,
            implied_volatility=implied_volatility
        )

        st.subheader(f"Dettaglio Strategia: {selected_strategy_name}")

        # --- NUOVA TABELLA DETTAGLIO GAMBE ---
        leg_data = []
        for leg in strategy_details["legs"]:
            leg_data.append({
                "Direzione": leg["direction"].capitalize(),
                "Quantità": leg["ratio"],
                "Tipo": leg["type"].capitalize(),
                "Strike": center_strike + leg.get("strike_offset", 0)
            })
        
        df_legs = pd.DataFrame(leg_data)
        st.dataframe(df_legs, use_container_width=True)
        
        st.markdown("---")

        # Dashboard delle Greche
        st.subheader("Dashboard delle Greche per Contratto")
        cols = st.columns(4)
        cols[0].metric("Delta", f"{greeks['delta']:.2f}")
        cols[1].metric("Gamma", f"{greeks['gamma']:.2f}")
        cols[2].metric("Theta", f"{greeks['theta']:.2f}")
        cols[3].metric("Vega", f"{greeks['vega']:.2f}")
        
        st.markdown("---")

        # Grafico P/L
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

# --- Contenuto Tab 2: Playbook (What-If) ---
with tab2:
    st.header("⚙️ Motore di Simulazione 'What-If'")
    st.markdown("Questa sezione è in fase di sviluppo (Prossimo Step).")
    st.info("Qui potrai definire scenari di mercato futuri e testare aggiustamenti sulla tua strategia, visualizzando l'impatto sul profilo di rischio in un grafico comparativo.", icon="🛠️")
    
    # Qui verrà implementata la logica della Fase 3
    # Esempio di struttura futura:
    # st.subheader("Definisci lo Scenario Futuro")
    # new_price = st.slider(...)
    # days_passed = st.slider(...)
    # st.subheader("Aggiustamenti Consigliati")
    # if st.button("Rolla la strategia"):
    #     # ... logica di aggiustamento ...
