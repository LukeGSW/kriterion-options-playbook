import streamlit as st
import numpy as np
import copy
from core.financial_calcs import calculate_pnl_and_greeks
from core.plotting import create_pnl_chart
from playbook.adjustments import roll_strategy

def render_playbook_tab():
    """
    Renderizza l'intera interfaccia e la logica per la tab "Playbook (What-If)".
    """
    st.header("⚙️ Motore di Simulazione 'What-If'")

    if "snapshot" not in st.session_state:
        st.info("Vai alla tab 'Analisi Strategia', imposta una posizione e clicca su '📸 Usa questo grafico come riferimento per il Playbook' per iniziare.")
        return

    snapshot = st.session_state.snapshot

    st.subheader("1. Definisci uno Scenario di Mercato (vs. Riferimento)")
    cols = st.columns(2)
    with cols[0]:
        sim_price_change_percent = st.slider("Variazione Prezzo Sottostante (%)", -50, 50, 0, key="sim_price_slider")
    with cols[1]:
        sim_days_passed = st.slider("Giorni Trascorsi", 0, snapshot['params']['base_days_to_expiration'], 0, key="sim_days_slider")

    # Determina se l'utente sta attivamente simulando (slider non a zero)
    is_simulating = not (sim_price_change_percent == 0 and sim_days_passed == 0)

    # Determina la strategia da usare (modificata o quella dello snapshot)
    if "current_adjusted_strategy" in st.session_state:
        legs_to_simulate = st.session_state.current_adjusted_strategy["legs"]
        name_to_simulate = st.session_state.current_adjusted_strategy["name"]
        is_adjusted = True
    else:
        legs_to_simulate = snapshot["legs"]
        name_to_simulate = snapshot["name"]
        is_adjusted = False

    # Se gli slider sono a zero e non ci sono aggiustamenti, mostra semplicemente lo snapshot
    if not is_simulating and not is_adjusted:
        pnl_T_main = snapshot['pnl_T']
        pnl_exp_main = snapshot['pnl_exp']
        greeks_main, _ = calculate_pnl_and_greeks(strategy_legs=snapshot['legs'], **snapshot['params']) # Greche sempre live
        main_price_range = snapshot['range']
        main_dte = snapshot['params']['base_days_to_expiration']
        show_original_overlay = False
    else: # Altrimenti, esegui la simulazione
        simulated_params = copy.deepcopy(snapshot['params'])
        new_underlying_price = simulated_params['underlying_price'] * (1 + sim_price_change_percent / 100.0)
        new_price_range = np.linspace(new_underlying_price * 0.7, new_underlying_price * 1.3, 200)
        simulated_params.update({
            'underlying_price': new_underlying_price,
            'underlying_range': new_price_range,
            'base_days_to_expiration': snapshot['params']['base_days_to_expiration'] - sim_days_passed
        })
        pnl_T_main, pnl_exp_main, greeks_main = calculate_pnl_and_greeks(
            strategy_legs=legs_to_simulate, **simulated_params
        )
        main_price_range = new_price_range
        main_dte = simulated_params['base_days_to_expiration']
        show_original_overlay = True

    st.markdown("---")
    sim_cols = st.columns([1.5, 1, 1, 1, 1])
    with sim_cols[0]:
        price_for_metric = new_underlying_price if is_simulating else snapshot['params']['underlying_price']
        idx = np.abs(main_price_range - price_for_metric).argmin()
        pnl_at_sim_price = pnl_T_main[idx]
        st.metric("P/L Attuale (Simulato)", f"{pnl_at_sim_price:,.2f} $")
    with sim_cols[1]:
        st.metric("Delta", f"{greeks_main['delta']:.2f}")
    with sim_cols[2]:
        st.metric("Gamma", f"{greeks_main['gamma']:.2f}")
    with sim_cols[3]:
        st.metric("Theta", f"{greeks_main['theta']:.2f}")
    with sim_cols[4]:
        st.metric("Vega", f"{greeks_main['vega']:.2f}")

    st.markdown("---")

    st.subheader("2. Applica un Aggiustamento Strutturale")
    roll_cols = st.columns(3)
    with roll_cols[0]:
        if st.button("Rolla su (Roll Up) 📈"):
            new_legs = roll_strategy(legs_to_simulate, 5)
            if new_legs:
                st.session_state.current_adjusted_strategy = {"name": f"{snapshot['name']} (Modificato)", "legs": new_legs}
                st.rerun()
    with roll_cols[1]:
        if st.button("Rolla giù (Roll Down) 📉"):
            new_legs = roll_strategy(legs_to_simulate, -5)
            if new_legs:
                st.session_state.current_adjusted_strategy = {"name": f"{snapshot['name']} (Modificato)", "legs": new_legs}
                st.rerun()
    with roll_cols[2]:
        if st.button("Reset Aggiustamenti"):
            if "current_adjusted_strategy" in st.session_state:
                del st.session_state.current_adjusted_strategy
            st.rerun()

    st.markdown("---")
    st.subheader("3. Grafico Comparativo Profit/Loss")

    pnl_chart = create_pnl_chart(
        underlying_range=main_price_range,
        pnl_at_T=pnl_T_main,
        pnl_at_expiration=pnl_exp_main,
        strategy_name=f"{name_to_simulate} (Simulazione)" if (is_simulating or is_adjusted) else name_to_simulate,
        days_to_expiration=main_dte,
        original_pnl_at_T=snapshot['pnl_T'] if show_original_overlay else None,
        original_pnl_at_expiration=snapshot['pnl_exp'] if show_original_overlay else None,
        original_underlying_range=snapshot['range'] if show_original_overlay else None
    )

    st.plotly_chart(pnl_chart, use_container_width=True)
