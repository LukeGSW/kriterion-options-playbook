import streamlit as st
from core.financial_calcs import calculate_pnl_and_greeks
from core.plotting import create_pnl_chart
from playbook.adjustments import roll_strategy # Modificato import

def render_playbook_tab(strategy_details, base_params):
    """
    Renderizza l'intera interfaccia e la logica per la tab "Playbook (What-If)".
    """
    st.header("⚙️ Motore di Simulazione 'What-If'")

    if not strategy_details or not strategy_details.get("legs"):
        st.warning("Seleziona una strategia valida dalla tab 'Analisi Strategia' per iniziare una simulazione.")
        return

    # Inizializza o resetta lo stato della simulazione se la strategia base cambia
    if "original_strategy" not in st.session_state or st.session_state.original_strategy['name'] != base_params['name']:
        st.session_state.original_strategy = {"name": base_params['name'], "legs": strategy_details["legs"]}
        if "current_adjusted_strategy" in st.session_state:
            del st.session_state.current_adjusted_strategy

    # Determina quali gambe usare per l'aggiustamento: le ultime modificate o le originali
    legs_to_adjust = st.session_state.get("current_adjusted_strategy", st.session_state.original_strategy)["legs"]

    st.subheader("1. Definisci uno Scenario di Mercato")
    cols = st.columns(2)
    with cols[0]:
        sim_price = st.slider("Variazione Prezzo Sottostante (%)", -50, 50, 0, key="sim_price_slider")
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

    st.subheader("3. Grafico Comparativo Profit/Loss")

    price_range = base_params['price_range']
    pnl_T_orig, pnl_exp_orig, _ = calculate_pnl_and_greeks(
        strategy_legs=st.session_state.original_strategy['legs'],
        **base_params['calc_params']
    )

    # Se c'è una strategia modificata, usala come principale
    if "current_adjusted_strategy" in st.session_state:
        main_strategy = st.session_state.current_adjusted_strategy
        show_original = True
    else:
        main_strategy = st.session_state.original_strategy
        show_original = False

    pnl_T_main, pnl_exp_main, _ = calculate_pnl_and_greeks(
        strategy_legs=main_strategy['legs'],
        **base_params['calc_params']
    )

    pnl_chart = create_pnl_chart(
        underlying_range=price_range,
        pnl_at_T=pnl_T_main,
        pnl_at_expiration=pnl_exp_main,
        strategy_name=main_strategy['name'],
        days_to_expiration=base_params['dte'],
        original_pnl_at_T=pnl_T_orig if show_original else None,
        original_pnl_at_expiration=pnl_exp_orig if show_original else None
    )

    st.plotly_chart(pnl_chart, use_container_width=True)
