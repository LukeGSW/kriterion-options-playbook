# playbook/playbook_ui.py
import copy
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from core.financial_calcs import calculate_pnl_and_greeks

def _build_chart(x, pl_expiry_frozen, pl_now, spot):
    fig = go.Figure()
    # Curva a scadenza - FISSA (dallo snapshot)
    fig.add_trace(go.Scatter(
        x=x, y=pl_expiry_frozen, name="P/L a scadenza (fisso)", mode="lines"
    ))
    # Curva now (T+Δ) - dipende dagli slider
    fig.add_trace(go.Scatter(
        x=x, y=pl_now, name="P/L now (scenario)", mode="lines",
        line=dict(dash="dot")
    ))
    # Spot scenario
    fig.add_vline(x=float(spot), line_width=1, line_dash="dash", opacity=0.7)

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Prezzo sottostante",
        yaxis_title="Profit / Loss"
    )
    return fig

def render_playbook_tab():
    st.subheader("Playbook (What-If)")
    snap = st.session_state.get("snapshot")

    if not snap:
        st.info("📌 Prima crea uno snapshot dalla tab *Analisi Strategia* con il pulsante apposito.")
        return

    # Migrazione di snapshot “vecchi” (senza timestamp): li normalizziamo
    if "timestamp" not in snap:
        snap = copy.deepcopy(snap)
        snap["timestamp"] = datetime.now().isoformat(timespec="seconds")
        st.session_state.snapshot = snap

    # --- Lettura baseline congelata ---
    base_params = snap["params"]
    x_grid     = np.array(base_params["underlying_range"], copy=True)  # stessa griglia della baseline
    frozen_exp = np.array(snap["pnl_exp"], copy=True)                  # curva a scadenza FISSA
    legs       = snap["legs"]

    base_S      = float(base_params["underlying_price"])
    base_days   = int(base_params["base_days_to_expiration"])
    base_iv     = float(base_params["implied_volatility"])
    center_strk = float(base_params["center_strike"])

    st.caption(f"Baseline fissata da: **{snap.get('name', '(sconosciuta)')}** — Snapshot: {snap.get('timestamp', '-')}")

    # Slider What-If (chiavi isolate e limiti coerenti alla griglia)
    s_min, s_max = float(np.min(x_grid)), float(np.max(x_grid))
    step_s = float(max(0.01, (s_max - s_min) / 200.0))

    c1, c2, c3 = st.columns(3)
    with c1:
        S_now = st.slider("Prezzo spot scenario", min_value=s_min, max_value=s_max,
                          value=float(base_S), step=step_s, key="whatif_S")
    with c2:
        days_passed = st.slider("Giorni trascorsi", 0, 365, 0, 1, key="whatif_days")
    with c3:
        iv_shift = st.slider("Shift IV (%)", -50, 50, 0, 1, key="whatif_iv")

    # --- Calcolo esclusivamente del P/L 'at now' ---
    remaining_days = max(0, base_days - int(days_passed))
    iv_scn = max(0.01, base_iv * (1.0 + iv_shift / 100.0))

    scenario_params = {
        "center_strike": center_strk,          # NON cambia
        "underlying_range": x_grid,            # identica alla baseline
        "base_days_to_expiration": remaining_days,
        "implied_volatility": iv_scn,
        "underlying_price": float(S_now)       # usato per greche/marker
    }

    pnl_T_now, _pnl_exp_ignore, greeks = calculate_pnl_and_greeks(
        strategy_legs=legs, **scenario_params
    )
    # IMPORTANTISSIMO: ignoriamo QUALSIASI 'pnl_exp' di scenario (la scadenza resta congelata)

    # --- Riquadro "At Now" ---
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Spot", f"{S_now:.2f}")
    m2.metric("Giorni residui", f"{remaining_days}")
    m3.metric("IV (%)", f"{iv_scn:.1f}")
    m4.metric("Delta", f"{greeks['delta']:.2f}")
    m5.metric("Theta", f"{greeks['theta']:.2f}")
    g1, g2, g3 = st.columns(3)
    g1.metric("Gamma", f"{greeks['gamma']:.4f}")
    g2.metric("Vega",  f"{greeks['vega']:.2f}")
    g3.caption("La curva a scadenza resta congelata; muovendo gli slider varia solo il P/L 'now'.")

    # --- Grafico: disegno diretto, nessun ricalcolo della scadenza ---
    fig = _build_chart(x_grid, frozen_exp, np.array(pnl_T_now, copy=True), S_now)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    if st.button("❌ Rimuovi snapshot (riparti da Analisi Strategia)", key="clear_snapshot"):
        del st.session_state["snapshot"]
        # pulizia dei controlli what-if
        for k in list(st.session_state.keys()):
            if str(k).startswith("whatif_"):
                del st.session_state[k]
        st.success("Snapshot rimosso. Torna su 'Analisi Strategia' per fissarne uno nuovo.")
