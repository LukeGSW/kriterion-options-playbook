import streamlit as st
import numpy as np
from core.financial_calcs import calculate_pnl_and_greeks
from core.plotting import create_pnl_chart
from playbook.adjustments import roll_strategy

def render_playbook_tab(strategy_details, base_params, current_legs):
    """
    Renderizza l'intera interfaccia e la logica per la tab "Playbook (What-If)".
    """
    st.header("⚙️ Motore di Simulazione 'What-If'")

    if not strategy_details or not current_legs:
        st.warning("Seleziona una strategia valida dalla tab 'Analisi Strategia' per iniziare una simulazione.")
        return

    # --- NUOVO: Blocco di validazione per snapshot di versioni precedenti ---
    # Se lo snapshot esiste ma non ha i dati pre-calcolati, viene considerato invalido e rimosso.
    if "snapshot" in st.session_state and "pnl_T" not in st.session_state.snapshot:
        del st.session_state.snapshot
        st.warning("È stato rilevato uno snapshot di una versione precedente e rimosso. Per favore, clicca di nuovo su 'Fissa Strategia'.")

    # Pulsante per creare/aggiornare lo snapshot di riferimento
    if st.button("📸 Fissa Strategia Corrente come Riferimento"):
        pnl_T_snapshot, pnl_exp_snapshot, _ = calculate_pnl_and_greeks(
            strategy_legs=current_legs,
            **base_params['calc_params']
        )
        st.session_state.snapshot = {
            "name": base_params['name'],
            "legs": current_legs,
            "params": base_params['calc_params'].copy(),
            "pnl_T": pnl_T_snapshot,
            "pnl_exp": pnl_exp_snapshot,
            "range": base_params['calc_params']['underlying_range']
        }
        if "current_adjusted_strategy" in st.session_state:
            del st.session_state.current_adjusted_strategy
        st.success(f"Snapshot creato per '{base_params['name']}'. Ora puoi usare gli slider e gli aggiustamenti.")
        st.rerun() # Forza un rerun per mostrare subito la simulazione
    
    st.markdown("---")

    if "snapshot" not in st.session_state:
        st.info("Imposta una strategia e i parametri nella prima tab, poi clicca il pulsante qui sopra per creare uno snapshot e iniziare la simulazione.")
        return

    # --- Sezione di Simulazione ---
    snapshot = st.session_state.snapshot

    st.subheader("1. Definisci uno Scenario di Mercato (vs. Snapshot)")
    cols = st.columns(2)
    with cols[0]:
        sim_price_change_percent = st.slider("Variazione Prezzo Sottostante (%)", -50, 50, 0, key="sim_price_slider")
    with cols[1]:
        sim_days_passed = st.slider("Giorni Trascorsi", 0, snapshot['params']['base_days_to_expiration'], 0, key="sim_days_slider")

    legs_to_adjust = st.session_state.get("current_adjusted_strategy", snapshot).get("legs")
    current_strategy_name = st.session_state.get("current_adjusted_strategy", snapshot).get("name")

    simulated_params = snapshot['params'].copy()
    new_underlying_price = simulated_params['underlying_price'] * (1 + sim_price_change_percent / 100.0)
    new_price_range = np.linspace(new_underlying_price * 0.7, new_underlying_price * 1.3, 200)
    simulated_params.update({
        'underlying_price': new_underlying_price,
        'underlying_range': new_price_range,
        'base_days_to_expiration': snapshot['params']['base_days_to_expiration'] - sim_days_passed
    })

    pnl_T_main, pnl_exp_main, greeks_main = calculate_pnl_and_greeks(
        strategy_legs=legs_to_adjust,
        **simulated_params
    )
    
    st.markdown("---")
    sim_cols = st.columns([1.5, 1, 1, 1, 1])
    with sim_cols[0]:
        idx = np.abs(new_price_range - new_underlying_price).argmin()
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
            new_legs = roll_strategy(legs_to_adjust, 5)
            if new_legs:
                st.session_state.current_adjusted_strategy = {"name": f"{snapshot['name']} (Modificato)", "legs": new_legs}
                st.rerun()
    with roll_cols[1]:
        if st.button("Rolla giù (Roll Down) 📉"):
            new_legs = roll_strategy(legs_to_adjust, -5)
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
        underlying_range=new_price_range,
        pnl_at_T=pnl_T_main,
        pnl_at_expiration=pnl_exp_main,
        strategy_name=f"{current_strategy_name} (Simulazione)",
        days_to_expiration=simulated_params['base_days_to_expiration'],
        original_pnl_at_T=snapshot['pnl_T'],
        original_pnl_at_expiration=snapshot['pnl_exp'],
        original_underlying_range=snapshot['range']
    )

    st.plotly_chart(pnl_chart, use_container_width=True)
