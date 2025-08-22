import numpy as np
from py_vollib.black_scholes_merton import black_scholes_merton
from py_vollib.black_scholes_merton.greeks.analytical import delta, gamma, theta, vega

# Flag per il tipo di opzione, richiesto da py_vollib
OPTION_TYPE = {'call': 'c', 'put': 'p'}

def calculate_pnl_and_greeks(
    strategy_legs, 
    center_strike, 
    underlying_range, 
    days_to_expiration, 
    implied_volatility,
    interest_rate=0.01, # Tasso risk-free
    dividend_yield=0.0  # Tasso di dividendo continuo (q)
    ):
    """
    Calcola P/L a una data intermedia, P/L a scadenza e le Greche aggregate.
    """
    # Inizializza i contenitori per i risultati
    pnl_at_T = np.zeros_like(underlying_range)
    pnl_at_expiration = np.zeros_like(underlying_range)
    
    total_delta = 0.0
    total_gamma = 0.0
    total_theta = 0.0
    total_vega = 0.0
    
    # Parametri temporali per i calcoli
    T = days_to_expiration / 365.0
    iv = implied_volatility / 100.0
    q = dividend_yield

    # Calcola il prezzo corrente di ogni gamba per determinare il costo/credito della strategia
    strategy_cost = 0
    current_underlying_price = underlying_range[np.abs(underlying_range - center_strike).argmin()]

    for leg in strategy_legs:
        strike = center_strike + leg.get("strike_offset", 0)
        flag = OPTION_TYPE[leg["type"]]
        
        # Calcolo del costo iniziale della gamba
        leg_price = black_scholes_merton(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        cost_multiplier = -1 if leg["direction"] == "long" else 1
        strategy_cost += leg_price * leg["ratio"] * cost_multiplier
        
        # Calcolo Greche (solo al prezzo corrente del sottostante)
        d = delta(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        g = gamma(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        t = theta(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        v = vega(flag, current_underlying_price, strike, T, interest_rate, iv, q)

        # Inverte il segno delle greche per le posizioni short
        short_multiplier = 1 if leg["direction"] == "long" else -1
        total_delta += d * leg["ratio"] * short_multiplier
        total_gamma += g * leg["ratio"] * short_multiplier
        total_theta += t * leg["ratio"] * short_multiplier
        total_vega += v * leg["ratio"] * short_multiplier
        
        # --- Calcolo P/L sul range di prezzi ---
        # 1. P/L a scadenza (valore intrinseco, già vettorizzato con numpy)
        payoff_expiration = np.zeros_like(underlying_range)
        if leg["type"] == "call":
            payoff_expiration = np.maximum(0, underlying_range - strike)
        else: # put
            payoff_expiration = np.maximum(0, strike - underlying_range)
        
        if leg["direction"] == "short":
            payoff_expiration *= -1
            
        pnl_at_expiration += payoff_expiration * leg["ratio"]

        # --- INIZIO BLOCCO MODIFICATO ---
        # 2. P/L a T (data intermedia) - Sostituito calcolo vettorizzato con un ciclo
        # per evitare l'errore ValueError nella libreria sottostante.
        
        leg_pnl_at_T_list = []
        for price_point in underlying_range:
            # Calcola il prezzo dell'opzione per un singolo punto di prezzo
            option_price = black_scholes_merton(flag, price_point, strike, T, interest_rate, iv, q)
            leg_pnl_at_T_list.append(option_price)
        
        # Converti la lista di risultati in un array numpy
        option_price_at_T = np.array(leg_pnl_at_T_list)
        
        if leg["direction"] == "short":
            option_price_at_T *= -1
        
        pnl_at_T += option_price_at_T * leg["ratio"]
        # --- FINE BLOCCO MODIFICATO ---

    # Normalizza il P/L rispetto al costo/credito iniziale
    pnl_at_T += strategy_cost
    pnl_at_expiration += strategy_cost
    
    greeks = {
        "delta": total_delta,
        "gamma": total_gamma,
        "theta": total_theta,
        "vega": total_vega
    }

    return pnl_at_T, pnl_at_expiration, greeks
