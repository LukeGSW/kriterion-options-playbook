import numpy as np

def calculate_payoff_at_expiration(strategy_legs, center_strike, underlying_range):
    """
    Calcola il P/L aggregato di una strategia alla scadenza.
    Per la Fase 1, gestisce solo il valore intrinseco.
    """
    total_payoff = np.zeros_like(underlying_range)

    for leg in strategy_legs:
        # Calcola lo strike effettivo della gamba
        strike = center_strike + leg.get("strike_offset", 0)
        
        payoff = np.zeros_like(underlying_range)
        
        if leg["type"] == "call":
            payoff = np.maximum(0, underlying_range - strike)
        elif leg["type"] == "put":
            payoff = np.maximum(0, strike - underlying_range)

        # Inverte il payoff per le posizioni short
        if leg["direction"] == "short":
            payoff *= -1
            
        total_payoff += payoff * leg["ratio"]

    return total_payoff
