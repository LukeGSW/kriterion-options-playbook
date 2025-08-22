import numpy as np
from py_vollib.black_scholes_merton import black_scholes_merton
from py_vollib.black_scholes_merton.greeks.analytical import delta, gamma, theta, vega

OPTION_TYPE = {'call': 'c', 'put': 'p'}
CONTRACT_MULTIPLIER = 100
DEFAULT_MONEYNESS_OFFSET = 0.10 # 10% per ITM/OTM

def get_strike(leg, center_strike, underlying_price):
    """Calcola lo strike effettivo di una gamba."""
    if 'strike_offset' in leg:
        return center_strike + leg['strike_offset']
    
    moneyness = leg.get('moneyness')
    if moneyness == 'ATM':
        return center_strike
    if moneyness == 'ITM':
        offset = underlying_price * DEFAULT_MONEYNESS_OFFSET
        return center_strike - offset if leg['type'] == 'call' else center_strike + offset
    if moneyness == 'OTM':
        offset = underlying_price * DEFAULT_MONEYNESS_OFFSET
        return center_strike + offset if leg['type'] == 'call' else center_strike - offset
    
    return center_strike # Default

def calculate_pnl_and_greeks(
    strategy_legs, 
    center_strike, 
    underlying_range, 
    base_days_to_expiration, 
    implied_volatility,
    interest_rate=0.01,
    dividend_yield=0.0
    ):
    pnl_at_T = np.zeros_like(underlying_range)
    pnl_at_expiration = np.zeros_like(underlying_range)
    
    total_delta = 0.0
    total_gamma = 0.0
    total_theta = 0.0
    total_vega = 0.0
    
    iv = implied_volatility / 100.0
    q = dividend_yield
    
    strategy_cost = 0
    current_underlying_price = underlying_range[np.abs(underlying_range - center_strike).argmin()]

    for leg in strategy_legs:
        if leg["type"] == 'stock':
            stock_pnl = np.zeros_like(underlying_range)
            direction_mult = 1 if leg['direction'] == 'long' else -1
            stock_pnl = (underlying_range - current_underlying_price) * direction_mult
            total_delta += 1 * leg["ratio"] * direction_mult
            # Il P/L dello stock è lineare e non dipende dal tempo, quindi è lo stesso a T e a scadenza
            pnl_at_expiration += stock_pnl
            pnl_at_T += stock_pnl
            continue

        # Gestione scadenze e strike dinamici
        leg_days_to_expiration = base_days_to_expiration + leg.get("expiry_offset", 0)
        T_leg = leg_days_to_expiration / 365.0
        T_leg = max(T_leg, 0.0001)

        strike = get_strike(leg, center_strike, current_underlying_price)
        flag = OPTION_TYPE[leg["type"]]
        
        # Calcolo costo iniziale e Greche (solo se la gamba non è già scaduta)
        if leg_days_to_expiration > 0:
            leg_price = black_scholes_merton(flag, current_underlying_price, strike, T_leg, interest_rate, iv, q)
            cost_multiplier = -1 if leg["direction"] == "long" else 1
            strategy_cost += leg_price * leg["ratio"] * cost_multiplier
        
            d = delta(flag, current_underlying_price, strike, T_leg, interest_rate, iv, q)
            g = gamma(flag, current_underlying_price, strike, T_leg, interest_rate, iv, q)
            t = theta(flag, current_underlying_price, strike, T_leg, interest_rate, iv, q)
            v = vega(flag, current_underlying_price, strike, T_leg, interest_rate, iv, q)

            short_multiplier = 1 if leg["direction"] == "long" else -1
            total_delta += d * leg["ratio"] * short_multiplier
            total_gamma += g * leg["ratio"] * short_multiplier
            total_theta += t * leg["ratio"] * short_multiplier
            total_vega += v * leg["ratio"] * short_multiplier

        # --- INIZIO BLOCCO LOGICA CORRETTA PER P/L A SCADENZA ---
        days_remaining_at_first_expiry = leg_days_to_expiration - base_days_to_expiration
        
        if days_remaining_at_first_expiry == 0:
            # Questa gamba scade ORA. Calcolo il suo valore intrinseco.
            payoff = np.maximum(0, underlying_range - strike) if leg["type"] == "call" else np.maximum(0, strike - underlying_range)
            if leg["direction"] == "short":
                payoff *= -1
            pnl_at_expiration += payoff * leg["ratio"]
        
        elif days_remaining_at_first_expiry > 0:
            # Questa gamba NON è ancora scaduta. Calcolo il suo valore teorico residuo.
            T_remaining = days_remaining_at_first_expiry / 365.0
            
            theoretical_value_list = []
            for price_point in underlying_range:
                price = black_scholes_merton(flag, price_point, strike, T_remaining, interest_rate, iv, q)
                theoretical_value_list.append(price)
            
            theoretical_value = np.array(theoretical_value_list)
            if leg["direction"] == "short":
                theoretical_value *= -1
            pnl_at_expiration += theoretical_value * leg["ratio"]
        # --- FINE BLOCCO LOGICA CORRETTA ---

        # Calcolo P/L a T (curva rossa) - la logica era già corretta
        leg_pnl_at_T_list = []
        if leg_days_to_expiration > 0:
            for price_point in underlying_range:
                option_price = black_scholes_merton(flag, price_point, strike, T_leg, interest_rate, iv, q)
                leg_pnl_at_T_list.append(option_price)
            option_price_at_T = np.array(leg_pnl_at_T_list)
        else:
            option_price_at_T = np.maximum(0, underlying_range - strike) if leg["type"] == "call" else np.maximum(0, strike - underlying_range)
        
        if leg["direction"] == "short":
            option_price_at_T *= -1
        pnl_at_T += option_price_at_T * leg["ratio"]

    # Finalizzazione P/L e Greche
    pnl_at_T += strategy_cost
    pnl_at_expiration += strategy_cost
    
    final_pnl_at_T = pnl_at_T * CONTRACT_MULTIPLIER
    final_pnl_at_expiration = pnl_at_expiration * CONTRACT_MULTIPLIER
    
    greeks = {
        "delta": total_delta * CONTRACT_MULTIPLIER,
        "gamma": total_gamma * CONTRACT_MULTIPLIER,
        "theta": total_theta * CONTRACT_MULTIPLIER,
        "vega": total_vega * CONTRACT_MULTIPLIER
    }

    return final_pnl_at_T, final_pnl_at_expiration, greeks
