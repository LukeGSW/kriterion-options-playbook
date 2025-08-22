import streamlit as st
from core.financial_calcs import calculate_pnl_and_greeks
from core.plotting import create_pnl_chart
from playbook.adjustments import roll_vertical_spread

def render_playbook_tab(strategy_details, base_params):
    """
    Renderizza l'intera interfaccia e la logica per la tab "Playbook (What-If)".
    """
    st.header("⚙️ Motore di Simulazione 'What-If'")

    # Controlla se la strategia selezionata è valida per la simulazione
    if not strategy_details or not strategy_details.get("legs"):
        st.warning("Seleziona una strategia valida dalla tab 'Analisi Strategia' per iniziare una simulazione.")
        return

    # Inizializza session_state per memorizzare lo stato della simulazione
    if "original_strategy" not in st.session_state or st.session_state.original_strategy['name'] != base_params['name']:
        st.session_state.original_strategy = {"name": base_params['name'], "legs": strategy_details["legs"]}
        if "adjusted_strategy" in st.session_state:
            del st.session_state.adjusted_strategy

    # --- UI per definire lo scenario (per ora non influenza la logica, solo UI) ---
    st.subheader("1. Definisci uno Scenario di Mercato")
    cols = st.columns(2)
    with cols[0]:
        sim_price = st.slider("Variazione Prezzo Sottostante (%)", -50, 50, 0)
    with cols[1]:
        sim_days_passed = st.slider("Giorni Trascorsi", 0, base_params['dte'], 0)

    st.markdown("---")

    # --- UI per gli aggiustamenti ---
    st.subheader("2. Applica un Aggiustamento")
    
    # Mostra pulsanti di aggiustamento solo per strategie compatibili (es. Vertical Spreads)
    if len(st.session_state.original_strategy['legs']) == 2:
        st.markdown("**Aggiustamenti per Vertical Spread:**")
        roll_cols = st.columns(2)
        with roll_cols[0]:
            if st.button("Rolla su (Roll Up) 📈"):
                new_legs = roll_vertical_spread(st.session_state.original_strategy['legs'], 5)
                st.session_state.adjusted_strategy = {"name": f"{base_params['name']} Rollato", "legs": new_legs}
        with roll_cols[1]:
            if st.button("Rolla giù (Roll Down) 📉"):
                new_legs = roll_vertical_spread(st.session_state.original_strategy['legs'], -5)
                st.session_state.adjusted_strategy = {"name": f"{base_params['name']} Rollato", "legs": new_legs}

    if st.button("Reset Aggiustamenti"):
        if "adjusted_strategy" in st.session_state:
            del st.session_state.adjusted_strategy
        st.rerun()

    st.markdown("---")

    # --- Calcolo e Visualizzazione Grafico Comparativo ---
    st.subheader("3. Grafico Comparativo Profit/Loss")

    # Calcola P/L per la strategia originale
    price_range = base_params['price_range']
    pnl_T_orig, pnl_exp_orig, _ = calculate_pnl_and_greeks(
        strategy_legs=st.session_state.original_strategy['legs'],
        **base_params['calc_params']
    )

    # Calcola P/L per la strategia aggiustata, se esiste
    pnl_T_adj, pnl_exp_adj, adjusted_legs_details = (None, None, None)
    if "adjusted_strategy" in st.session_state:
        pnl_T_adj, pnl_exp_adj, _ = calculate_pnl_and_greeks(
            strategy_legs=st.session_state.adjusted_strategy['legs'],
            **base_params['calc_params']
        )
        adjusted_legs_details = st.session_state.adjusted_strategy['legs']


    # Crea il grafico comparativo
    pnl_chart = create_pnl_chart(
        underlying_range=price_range,
        pnl_at_T=pnl_T_adj if "adjusted_strategy" in st.session_state else pnl_T_orig,
        pnl_at_expiration=pnl_exp_adj if "adjusted_strategy" in st.session_state else pnl_exp_orig,
        strategy_name=st.session_state.adjusted_strategy['name'] if "adjusted_strategy" in st.session_state else base_params['name'],
        days_to_expiration=base_params['dte'],
        # Passa i dati originali per il confronto
        original_pnl_at_T=pnl_T_orig if "adjusted_strategy" in st.session_state else None,
        original_pnl_at_expiration=pnl_exp_orig if "adjusted_strategy" in st.session_state else None
    )

    st.plotly_chart(pnl_chart, use_container_width=True)
