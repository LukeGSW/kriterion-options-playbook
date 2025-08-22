import streamlit as st
import numpy as np
import copy # <-- IMPORTAZIONE NECESSARIA PER LA COPIA PROFONDA
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

    # Pulsante per creare/aggiornare lo snapshot di riferimento
    if st.button("📸 Fissa Strategia Corrente come Riferimento"):
        # Esegui il calcolo UNA SOLA VOLTA al momento dello snapshot
        pnl_T_snapshot, pnl_exp_snapshot, greeks_snapshot = calculate_pnl_and_greeks(
            strategy_legs=current_legs,
            **base_params['calc_params']
        )
        # Salva i dati GIÀ CALCOLATI e una COPIA PROFONDA dei parametri
        st.session_state.snapshot = {
            "name": base_params['name'],
            "legs": current_legs,
            "params": copy.deepcopy(base_params['calc_params']), # <-- USA DEEPCOPY PER ISOLAMENTO TOTALE
            "pnl_T": pnl_T_snapshot,
            "pnl_exp": pnl_exp_snapshot,
            "range": base_params['calc_params']['underlying_range']
        }
        # Resetta gli aggiustamenti quando si crea un nuovo snapshot
        if "current_adjusted_strategy" in st.session_state:
            del st.session_state.current_adjusted_strategy
        st.success(f"Snapshot creato per '{base_params['name']}'.")
        st.rerun()

    st.markdown("---")

    # Tutta la logica di simulazione viene eseguita solo se lo snapshot esiste e è valido
    if "snapshot" not in st.session_state or "pnl_T" not in st.session_state.snapshot:
        st.info("Imposta una strategia e i parametri nella prima tab, poi clicca il pulsante qui sopra per creare uno snapshot e iniziare la simulazione.")
        return

    # Da qui in poi, usiamo solo dati dallo snapshot o creati ex-novo
    snapshot = st.session_state.snapshot

    st.subheader("1. Definisci uno Scenario di Mercato (vs. Snapshot)")
    cols = st.columns(2)
    with cols[0]:
        sim_price_change_percent = st.slider("Variazione Prezzo Sottostante (%)", -50, 50, 0, key="sim_price_slider")
    with cols[1]:
        sim_days_passed = st.slider("Giorni Trascorsi", 0, snapshot['params']['base_days_to_expiration'], 0, key="sim_days_slider")

    # Determina la strategia da usare (modificata o quella dello snapshot)
    legs_to_simulate = st.session_state.get("current_adjusted_strategy", snapshot).get("legs")
    name_to_simulate = st.session_state.get("current_adjusted_strategy", snapshot).get("name")

    # Prepara i parametri per la simulazione, partendo da una copia pulita dello snapshot
    simulated_params = copy.deepcopy(snapshot['params'])
    new_underlying_price = simulated_params['underlying_price'] * (1 + sim_price_change_percent / 100.0)
    new_price_range = np.linspace(new_underlying_price * 0.7, new_underlying_price * 1.3, 200)
    simulated_params.update({
        'underlying_price': new_underlying_price,
        'underlying_range': new_price_range,
        'base_days_to_expiration': snapshot['params']['base_days_to_expiration'] - sim_days_passed
    })

    # Calcola P/L e Greche per la strategia simulata
    pnl_T_sim, pnl_exp_sim, greeks_sim = calculate_pnl_and_greeks(
        strategy_legs=legs_to_simulate,
        **simulated_params
    )
    
    st.markdown("---")
    sim_cols = st.columns([1.5, 1, 1, 1, 1])
    with sim_cols[0]:
        idx = np.abs(new_price_range - new_underlying_price).argmin()
        pnl_at_sim_price = pnl_T_sim[idx]
        st.metric("P/L Attuale (Simulato)", f"{pnl_at_sim_price:,.2f} $")
    with sim_cols[1]:
        st.metric("Delta", f"{greeks_sim['delta']:.2f}")
    with sim_cols[2]:
        st.metric("Gamma", f"{greeks_sim['gamma']:.2f}")
    with sim_cols[3]:
        st.metric("Theta", f"{greeks_sim['theta']:.2f}")
    with sim_cols[4]:
        st.metric("Vega", f"{greeks_sim['vega']:.2f}")

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
        underlying_range=new_price_range,
        pnl_at_T=pnl_T_sim,
        pnl_at_expiration=pnl_exp_sim,
        strategy_name=f"{name_to_simulate} (Simulazione)",
        days_to_expiration=simulated_params['base_days_to_expiration'],
        original_pnl_at_T=snapshot['pnl_T'],
        original_pnl_at_expiration=snapshot['pnl_exp'],
        original_underlying_range=snapshot['range']
    )

    st.plotly_chart(pnl_chart, use_container_width=True)
