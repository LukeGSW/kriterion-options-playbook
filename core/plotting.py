import plotly.graph_objects as go
import numpy as np

def create_pnl_chart(underlying_range, pnl_at_T, pnl_at_expiration, strategy_name, days_to_expiration):
    """
    Genera il grafico P/L interattivo con Plotly, mostrando sia la curva a T che a scadenza.
    """
    fig = go.Figure()

    # Linea del P/L a scadenza (solida)
    fig.add_trace(go.Scatter(
        x=underlying_range, 
        y=pnl_at_expiration, 
        mode='lines', 
        name='P/L a Scadenza',
        line=dict(color='royalblue', width=3)
    ))

    # Linea del P/L a T (tratteggiata)
    fig.add_trace(go.Scatter(
        x=underlying_range, 
        y=pnl_at_T, 
        mode='lines', 
        name=f'P/L a T-{days_to_expiration} giorni',
        line=dict(color='firebrick', width=2, dash='dash')
    ))

    # Linea dello zero
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")

    # Calcolo punti di breakeven a scadenza
    sign_changes = np.where(np.diff(np.sign(pnl_at_expiration)))[0]
    for be_index in sign_changes:
        fig.add_vline(x=underlying_range[be_index], line_width=1, line_dash="dot", line_color="red",
                      annotation_text="Breakeven", annotation_position="top left")

    # Layout e titoli
    fig.update_layout(
        title=f"Profilo Rischio/Rendimento: {strategy_name}",
        xaxis_title="Prezzo Sottostante",
        yaxis_title="Profit / Loss",
        legend=dict(x=0.01, y=0.99, orientation="h"),
        template="plotly_white"
    )

    return fig
