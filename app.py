# app.py
import streamlit as st
import numpy as np
import pandas as pd
import copy
from datetime import datetime

from strategies.strategy_database import STRATEGY_DATABASE
from core.financial_calcs import calculate_pnl_and_greeks, get_strike
from core.plotting import create_pnl_chart

# =========================
# CONFIGURAZIONE PAGINA
# =========================
st.set_page_config(
    page_title="Kriterion Options Playbook",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Kriterion Options Playbook")
st.markdown("Il simulatore interattivo per strategie in opzioni.")

# =========================
# SIDEBAR: INPUT UTENTE
# =========================
st.sidebar.header("Parametri di Input")

categories = list(STRATEGY_DATABASE.keys())
selected_category = st.sidebar.selectbox("1. Scegli una Categoria", options=categories)

strategies_in_category = list(STRATEGY_DATABASE[selected_category].keys())
selected_strategy_name = st.sidebar.selectbox("2. Scegli una Strategia", options=strategies_in_category)

strategy_details = STRATEGY_DATABASE[selected_category][selected_strategy_name]
st.sidebar.info(strategy_details.get("description", ""))

if "note" in strategy_details:
    st.sidebar.warning(f'Nota: {strategy_details["note"]}')

st.sidebar.subheader("Aggiungi Sottostante (Opzionale)")
stock_position = st.sidebar.radio(
    "Aggiungi una posizione sul sottostante alla strategia",
    options=["Nessuno", "Long", "Short"],
    horizontal=True,
    label_visibility="collapsed"
)

st.sidebar.subheader("3. Parametri di Mercato")
underlying_price = st.sidebar.number_input("Prezzo Sottostante (S)", value=100.0, step=0.5)
center_strike = st.sidebar.number_input("Strike Centrale (K)", value=100.0, step=0.5)

st.sidebar.subheader("4. Parametri di Analisi")
base_days_to_expiration = st.sidebar.slider("Giorni alla Scadenza (base)", min_value=1, max_value=365, value=30)
implied_volatility = st.sidebar.slider("Volatilità Implicita (%)", min_value=5, max_value=150, value=20)

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["Analisi Strategia", "Playbook (What-If)"])

# =========================
# LOGICA STRATEGIA (LEGS)
# =========================
modified_legs = strategy_details.get("legs", []).copy()
final_strategy_name = selected_strategy_name

if stock_position != "Nessuno":
    has_stock_leg = any(leg.get("type") == "stock" for leg in modified_legs)
    if not has_stock_leg:
        modified_legs.append({
            "type": "stock",
            "direction": stock_position.lower(),
            "ratio": 1
        })
        final_strategy_name = f"{selected_strategy_name} + {stock_position} Stock"

# =========================
# TAB 1: ANALISI STRATEGIA
# =========================
with tab1:
    if not modified_legs:
        st.subheader(f"Strategia Logica: {final_strategy_name}")
        st.info("Questa è una strategia concettuale o una sequenza operativa.")
    else:
        # Griglia prezzi coerente e riusabile nel Playbook
        price_range = np.linspace(underlying_price * 0.7, underlying_price * 1.3, 200)

        calc_params = {
            "center_strike": center_strike,
            "underlying_range": price_range,
            "base_days_to_expiration": base_days_to_expiration,
            "implied_volatility": implied_volatility,
            "underlying_price": underlying_price
        }

        pnl_T, pnl_exp, greeks = calculate_pnl_and_greeks(
            strategy_legs=modified_legs, **calc_params
        )

        st.subheader(f"Dettaglio Strategia: {final_strategy_name}")

        # Tabella legs
        leg_data = []
        for leg in modified_legs:
            if leg["type"] == "stock":
                leg_strike = underlying_price
                scadenza_gg = "N/A"
            else:
                leg_strike = get_strike(leg, center_strike, underlying_price)
                scadenza_gg = str(base_days_to_expiration + leg.get("expiry_offset", 0))
            leg_data.append({
                "Direzione": leg["direction"].capitalize(),
                "Quantità": leg["ratio"],
                "Tipo": leg["type"].capitalize(),
                "Strike/Prezzo": f"{leg_strike:.2f}" if isinstance(leg_strike, (int, float)) else leg_strike,
                "Scadenza (gg)": scadenza_gg
            })
        df_legs = pd.DataFrame(leg_data)
        st.dataframe(df_legs, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Dashboard delle Greche per Contratto")
        cols = st.columns(4)
        cols[0].metric("Delta", f"{greeks['delta']:.2f}")
        cols[1].metric("Gamma", f"{greeks['gamma']:.2f}")
        cols[2].metric("Theta", f"{greeks['theta']:.2f}")
        cols[3].metric("Vega",  f"{greeks['vega']:.2f}")

        st.markdown("---")
        st.subheader("Grafico Profit/Loss")
        pnl_chart = create_pnl_chart(
            underlying_range=price_range,
            pnl_at_T=pnl_T,
            pnl_at_expiration=pnl_exp,
            strategy_name=final_strategy_name,
            days_to_expiration=base_days_to_expiration
        )
        st.plotly_chart(pnl_chart, use_container_width=True)

        st.markdown("---")
        st.subheader("Playbook")

        # Bottone: congela baseline per il What-If
        if st.button("📸 Usa questo grafico come riferimento per il Playbook", key="lock_baseline"):
            st.session_state.snapshot = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "name": final_strategy_name,
                "legs": copy.deepcopy(modified_legs),
                "params": copy.deepcopy(calc_params),   # contiene: center_strike, underlying_range, base_days_to_expiration, implied_volatility, underlying_price
                "pnl_T": pnl_T,                         # opzionale: utile per confronto visivo se servisse
                "pnl_exp": pnl_exp                      # <<< CURVA A SCADENZA CONGELATA
            }
            # Pulizia stato What-If (chiavi isolate)
            for k in list(st.session_state.keys()):
                if str(k).startswith("whatif_"):
                    del st.session_state[k]
            st.success(f"Snapshot creato per '{final_strategy_name}'. Vai alla tab 'Playbook'.")

        st.subheader("Analisi Qualitativa della Strategia")
        if "analysis" in strategy_details and isinstance(strategy_details["analysis"], dict):
            analysis = strategy_details["analysis"]
            st.markdown(f"**🎯 Quando utilizzarla:** {analysis.get('when_to_use', 'N/A')}")
            st.markdown("**🔍 Condizioni di Mercato:**")
            conditions = analysis.get('market_conditions', {})
            st.markdown(f"- **Ottimali:** {conditions.get('optimal', 'N/A')}")
            st.markdown(f"- **Sconsigliate:** {conditions.get('poor', 'N/A')}")
            st.markdown(f"**✨ Peculiarità:** {analysis.get('peculiarities', 'N/A')}")
        else:
            st.warning("Dati di analisi qualitativa non trovati.")

# =========================================
# TAB 2: PLAYBOOK (WHAT-IF) — SOLO P/L NOW
# =========================================
with tab2:
    st.subheader("Playbook (What-If)")
    snap = st.session_state.get("snapshot", None)

    if not snap:
        st.info("📌 Prima crea uno **snapshot** dalla tab *Analisi Strategia* con il pulsante '📸 Usa questo grafico come riferimento per il Playbook'.")
    else:
        # Header con info snapshot
        st.caption(f"Baseline fissata da: **{snap['name']}** — Snapshot: {snap['timestamp']}")
        base_params = snap["params"]
        base_days = int(base_params["base_days_to_expiration"])
        base_iv = float(base_params["implied_volatility"])
        base_S = float(base_params["underlying_price"])
        base_center = float(base_params["center_strike"])
        x_grid = base_params["underlying_range"]
        frozen_expiry_curve = snap["pnl_exp"]  # <<< NON si ricalcola mai in questa tab

        # Controlli What-If con chiavi dedicate
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            whatif_S = st.slider(
                "Prezzo spot scenario",
                min_value=float(max(0.01, base_S * 0.3)),
                max_value=float(base_S * 2.0),
                value=float(base_S),
                step=0.5,
                key="whatif_S"
            )
        with c2:
            whatif_days_passed = st.slider(
                "Giorni trascorsi",
                min_value=0,
                max_value=365,
                value=0,
                step=1,
                key="whatif_days"
            )
        with c3:
            whatif_iv_shift = st.slider(
                "Shift IV (%)",
                min_value=-50,
                max_value=50,
                value=0,
                step=1,
                key="whatif_iv"
            )

        # Calcolo parametri scenario (SOLO P/L NOW)
        # Giorni residui: base_days - giorni trascorsi (>= 0)
        remaining_days = max(0, base_days - int(whatif_days_passed))
        scenario_iv = max(0.01, base_iv * (1.0 + whatif_iv_shift / 100.0))

        scenario_params = {
            "center_strike": base_center,          # NON si sposta
            "underlying_range": x_grid,            # stessa griglia della baseline
            "base_days_to_expiration": remaining_days,
            "implied_volatility": scenario_iv,
            "underlying_price": float(whatif_S)
        }

        # Ricalcolo SOLO della curva "now" con tempo residuo
        pnl_T_scn, _, greeks_scn = calculate_pnl_and_greeks(
            strategy_legs=snap["legs"],
            **scenario_params
        )
        # NB: ignoriamo il secondo valore (pnl_exp) di scenario: la scadenza resta congelata

        st.markdown("---")
        st.subheader("Greche (Scenario)")
        cols2 = st.columns(4)
        cols2[0].metric("Delta", f"{greeks_scn['delta']:.2f}")
        cols2[1].metric("Gamma", f"{greeks_scn['gamma']:.2f}")
        cols2[2].metric("Theta", f"{greeks_scn['theta']:.2f}")
        cols2[3].metric("Vega",  f"{greeks_scn['vega']:.2f}")

        st.markdown("---")
        st.subheader("Grafico Profit/Loss — Curva a Scadenza FISSA (baseline) + P/L Now (scenario)")
        chart = create_pnl_chart(
            underlying_range=x_grid,
            pnl_at_T=pnl_T_scn,                     # << SOLO questa cambia
            pnl_at_expiration=frozen_expiry_curve,  # << FISSA dalla baseline
            strategy_name=snap["name"],
            days_to_expiration=remaining_days
        )
        st.plotly_chart(chart, use_container_width=True)

        # Pulsante per invalidare lo snapshot (se l'utente vuole ripartire)
        st.markdown("---")
        c_left, c_right = st.columns([1, 3])
        with c_left:
            if st.button("❌ Rimuovi snapshot", key="clear_snapshot"):
                del st.session_state["snapshot"]
                # pulizia controlli what-if
                for k in list(st.session_state.keys()):
                    if str(k).startswith("whatif_"):
                        del st.session_state[k]
                st.success("Snapshot rimosso. Torna su 'Analisi Strategia' per fissarne uno nuovo.")
