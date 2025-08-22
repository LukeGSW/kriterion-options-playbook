import streamlit as st
import numpy as np
from core.financial_calcs import calculate_pnl_and_greeks
from core.plotting import create_pnl_chart
from playbook.adjustments import roll_strategy

def render_playbook_tab(strategy_details, base_params):
    """
    Renderizza l'intera interfaccia e la logica per la tab "Playbook (What-If)".
    """
    st.header("⚙️ Motore di Simulazione 'What-If'")

    if not strategy_details or not strategy_details.get("legs"):
        st.warning("Seleziona una strategia valida dalla tab 'Analisi Strategia' per iniziare una simulazione.")
        return

    if "original_strategy" not in st.session_state or st.session_state.original_strategy['name'] != base_params['name']:
        st.session_state.original_strategy = {"name": base_params['name'], "legs": strategy_details["legs"]}
        if "current_adjusted_strategy" in st.session_state:
            del st.session_state.current_adjusted_strategy

    legs_to_adjust = st.session_state.get("current_adjusted_strategy", st.session_state.original_strategy)["legs"]

    st.subheader("1. Definisci uno Scenario di Mercato")
    cols = st.columns(2)
    with cols[0]:
        sim_price_change_percent = st.slider("Variazione Prezzo Sottostante (%)", -50, 50, 0, key="sim_price_slider")
    with cols[1]:
        sim_days_passed = st.slider("Giorni Trascorsi", 0, base_params['dte'], 0, key="sim_days_slider")

    st.markdown("---")

    st.subheader("2. Applica un Aggiustamento")
    
    st.markdown("**Aggiustamenti di Roll:**")
    roll_cols = st.columns(2)
    with roll_cols[0]:
        if st.button("Rolla su (Roll Up) 📈"):
            new_legs = roll_strategy(legs_to_adjust, 5)
            if new_legs:
                st.session_state.current_adjusted_strategy = {"name": f"{base_params['name']} (Modificato)", "legs": new_legs}
                st.rerun()

    with roll_cols[1]:
        if st.button("Rolla giù (Roll Down) 📉"):
            new_legs = roll_strategy(legs_to_adjust, -5)
            if new_legs:
                st.session_state.current_adjusted_strategy = {"name": f"{base_params['name']} (Modificato)", "legs": new_legs}
                st.rerun()

    if st.button("Reset Aggiustamenti"):
        if "current_adjusted_strategy" in st.session_state:
            del st.session_state.current_adjusted_strategy
        st.rerun()

    st.markdown("---")

    st.subheader("3. Grafico Comparativo Profit/Loss (Simulato)")

    # Calcola P/L per la strategia originale (con i parametri base)
    pnl_T_orig, pnl_exp_orig, _ = calculate_pnl_and_greeks(
        strategy_legs=st.session_state.original_strategy['legs'],
        **base_params['calc_params']
    )

    main_strategy = st.session_state.get("current_adjusted_strategy", st.session_state.original_strategy)
    show_original_overlay = "current_adjusted_strategy" in st.session_state

    # Crea un nuovo set di parametri per la simulazione basato sui valori degli slider
    simulated_params = base_params['calc_params'].copy()
    
    new_underlying_price = simulated_params['underlying_price'] * (1 + sim_price_change_percent / 100.0)
    new_price_range = np.linspace(new_underlying_price * 0.7, new_underlying_price * 1.3, 200)

    simulated_params['underlying_price'] = new_underlying_price
    simulated_params['underlying_range'] = new_price_range
    simulated_params['base_days_to_expiration'] = base_params['dte'] - sim_days_passed
    
    pnl_T_main, pnl_exp_main, _ = calculate_pnl_and_greeks(
        strategy_legs=main_strategy['legs'],
        **simulated_params
    )
    
    # Crea il grafico passando entrambi gli assi X (originale e simulato)
    pnl_chart = create_pnl_chart(
        underlying_range=new_price_range,
        pnl_at_T=pnl_T_main,
        pnl_at_expiration=pnl_exp_main,
        strategy_name=f"{main_strategy['name']} (Simulazione)",
        days_to_expiration=simulated_params['base_days_to_expiration'],
        original_pnl_at_T=pnl_T_orig if show_original_overlay else None,
        original_pnl_at_expiration=pnl_exp_orig if show_original_overlay else None,
        original_underlying_range=base_params['calc_params']['underlying_range'] if show_original_overlay else None # <-- PASSAGGIO ASSE X ORIGINALE
    )

    st.plotly_chart(pnl_chart, use_container_width=True)
