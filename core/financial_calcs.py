import numpy as np
from py_vollib.black_scholes_merton import black_scholes_merton
from py_vollib.black_scholes_merton.greeks.analytical import delta, gamma, theta, vega

# Flag per il tipo di opzione, richiesto da py_vollib
OPTION_TYPE = {'call': 'c', 'put': 'p'}
CONTRACT_MULTIPLIER = 100 # Moltiplicatore standard per opzioni su azioni

def calculate_pnl_and_greeks(
    strategy_legs, 
    center_strike, 
    underlying_range, 
    days_to_expiration, 
    implied_volatility,
    interest_rate=0.01,
    dividend_yield=0.0
    ):
    """
    Calcola P/L e Greche, applicando il moltiplicatore del contratto (x100).
    """
    pnl_at_T = np.zeros_like(underlying_range)
    pnl_at_expiration = np.zeros_like(underlying_range)
    
    total_delta = 0.0
    total_gamma = 0.0
    total_theta = 0.0
    total_vega = 0.0
    
    T = days_to_expiration / 365.0
    iv = implied_volatility / 100.0
    q = dividend_yield
    
    strategy_cost = 0
    current_underlying_price = underlying_range[np.abs(underlying_range - center_strike).argmin()]

    for leg in strategy_legs:
        strike = center_strike + leg.get("strike_offset", 0)
        flag = OPTION_TYPE[leg["type"]]
        
        leg_price = black_scholes_merton(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        cost_multiplier = -1 if leg["direction"] == "long" else 1
        strategy_cost += leg_price * leg["ratio"] * cost_multiplier
        
        d = delta(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        g = gamma(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        t = theta(flag, current_underlying_price, strike, T, interest_rate, iv, q)
        v = vega(flag, current_underlying_price, strike, T, interest_rate, iv, q)

        short_multiplier = 1 if leg["direction"] == "long" else -1
        total_delta += d * leg["ratio"] * short_multiplier
        total_gamma += g * leg["ratio"] * short_multiplier
        total_theta += t * leg["ratio"] * short_multiplier
        total_vega += v * leg["ratio"] * short_multiplier
        
        payoff_expiration = np.zeros_like(underlying_range)
        if leg["type"] == "call":
            payoff_expiration = np.maximum(0, underlying_range - strike)
        else:
            payoff_expiration = np.maximum(0, strike - underlying_range)
        
        if leg["direction"] == "short":
            payoff_expiration *= -1
        pnl_at_expiration += payoff_expiration * leg["ratio"]

        leg_pnl_at_T_list = []
        for price_point in underlying_range:
            option_price = black_scholes_merton(flag, price_point, strike, T, interest_rate, iv, q)
            leg_pnl_at_T_list.append(option_price)
        
        option_price_at_T = np.array(leg_pnl_at_T_list)
        if leg["direction"] == "short":
            option_price_at_T *= -1
        pnl_at_T += option_price_at_T * leg["ratio"]

    pnl_at_T += strategy_cost
    pnl_at_expiration += strategy_cost
    
    # Applica il moltiplicatore del contratto a tutti i risultati finali.
    final_pnl_at_T = pnl_at_T * CONTRACT_MULTIPLIER
    final_pnl_at_expiration = pnl_at_expiration * CONTRACT_MULTIPLIER
    
    greeks = {
        "delta": total_delta * CONTRACT_MULTIPLIER,
        "gamma": total_gamma * CONTRACT_MULTIPLIER,
        "theta": total_theta * CONTRACT_MULTIPLIER,
        "vega": total_vega * CONTRACT_MULTIPLIER
    }

    return final_pnl_at_T, final_pnl_at_expiration, greeks
