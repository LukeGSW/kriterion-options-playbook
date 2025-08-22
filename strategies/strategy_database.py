STRATEGY_DATABASE = {
    "1. Posizioni Base & Sintetiche": {
        "Long Stock": {"legs": [{"type": "stock", "direction": "long", "ratio": 1}], "description": "Acquisto di 100 azioni. Rialzista, Delta 100."},
        "Short Stock": {"legs": [{"type": "stock", "direction": "short", "ratio": 1}], "description": "Vendita allo scoperto di 100 azioni. Ribassista, Delta -100."},
        "Long Call": {"legs": [{"type": "call", "direction": "long", "ratio": 1}], "description": "Acquisto di un'opzione Call. Rialzista, rischio limitato."},
        "Short Call": {"legs": [{"type": "call", "direction": "short", "ratio": 1}], "description": "Vendita di un'opzione Call. Ribassista/Laterale, rischio illimitato."},
        "Long Put": {"legs": [{"type": "put", "direction": "long", "ratio": 1}], "description": "Acquisto di un'opzione Put. Ribassista, rischio limitato."},
        "Short Put": {"legs": [{"type": "put", "direction": "short", "ratio": 1}], "description": "Vendita di un'opzione Put (Cash-Secured). Rialzista/Laterale."},
        "Synthetic Long Stock": {"legs": [{"type": "call", "direction": "long", "ratio": 1}, {"type": "put", "direction": "short", "ratio": 1}], "description": "Long Call + Short Put. Replica un'esposizione long sul sottostante."},
        "Synthetic Short Stock": {"legs": [{"type": "call", "direction": "short", "ratio": 1}, {"type": "put", "direction": "long", "ratio": 1}], "description": "Short Call + Long Put. Replica un'esposizione short sul sottostante."},
    },
    "2. Covered & Protective": {
        "Covered Call": {"legs": [{"type": "stock", "direction": "long", "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 10, "ratio": 1}], "description": "Long Stock + Short Call OTM. Strategia di income, limita il potenziale di rialzo."},
        "Protective Put": {"legs": [{"type": "stock", "direction": "long", "ratio": 1}, {"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1}], "description": "Long Stock + Long Put OTM. Limita il rischio al ribasso, una vera assicurazione."},
        "Collar": {"legs": [{"type": "stock", "direction": "long", "ratio": 1}, {"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 10, "ratio": 1}], "description": "Long Stock + Protective Put + Covered Call. Protezione a costo zero o ridotto."},
    },
    "3. Vertical Spreads": {
        "Bull Call Spread (Debit)": {"legs": [{"type": "call", "direction": "long", "strike_offset": -5, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1}], "description": "Rialzista, a rischio e rendimento definiti."},
        "Bear Call Spread (Credit)": {"legs": [{"type": "call", "direction": "short", "strike_offset": -5, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 5, "ratio": 1}], "description": "Ribassista/laterale, a rischio e rendimento definiti."},
        "Bull Put Spread (Credit)": {"legs": [{"type": "put", "direction": "short", "strike_offset": 5, "ratio": 1}, {"type": "put", "direction": "long", "strike_offset": -5, "ratio": 1}], "description": "Rialzista/laterale, a rischio e rendimento definiti."},
        "Bear Put Spread (Debit)": {"legs": [{"type": "put", "direction": "long", "strike_offset": 5, "ratio": 1}, {"type": "put", "direction": "short", "strike_offset": -5, "ratio": 1}], "description": "Ribassista, a rischio e rendimento definiti."},
    },
    "4. Ratio & Backspreads": {
        "Call Ratio Spread (Front)": {"legs": [{"type": "call", "direction": "long", "strike_offset": -5, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 2}], "description": "Long 1 Call + Short 2 Call OTM. Short volatility con view direzionale."},
        "Call Ratio Backspread": {"legs": [{"type": "call", "direction": "short", "strike_offset": -5, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 5, "ratio": 2}], "description": "Short 1 Call + Long 2 Call OTM. Rialzista e long volatility."},
        "Put Ratio Backspread": {"legs": [{"type": "put", "direction": "short", "strike_offset": 5, "ratio": 1}, {"type": "put", "direction": "long", "strike_offset": -5, "ratio": 2}], "description": "Short 1 Put + Long 2 Put OTM. Ribassista e long volatility."},
    },
    "5. Volatility (Straddle/Strangle)": {
        "Long Straddle": {"legs": [{"type": "call", "direction": "long", "ratio": 1}, {"type": "put", "direction": "long", "ratio": 1}], "description": "Long Call ATM + Long Put ATM. Long volatility puro."},
        "Short Straddle": {"legs": [{"type": "call", "direction": "short", "ratio": 1}, {"type": "put", "direction": "short", "ratio": 1}], "description": "Short Call ATM + Short Put ATM. Short volatility, massimo incasso di theta."},
        "Long Strangle": {"legs": [{"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1}], "description": "Long Put OTM + Long Call OTM. Long volatility, più economico di uno straddle."},
        "Short Strangle": {"legs": [{"type": "put", "direction": "short", "strike_offset": -10, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 10, "ratio": 1}], "description": "Short Put OTM + Short Call OTM. Short volatility con breakeven ampi."},
        "Strap (Long Vol - Bullish)": {"legs": [{"type": "call", "direction": "long", "ratio": 2}, {"type": "put", "direction": "long", "ratio": 1}], "description": "2 Long Call ATM + 1 Long Put ATM. Long volatility con un'inclinazione rialzista."},
        "Strip (Long Vol - Bearish)": {"legs": [{"type": "call", "direction": "long", "ratio": 1}, {"type": "put", "direction": "long", "ratio": 2}], "description": "1 Long Call ATM + 2 Long Put ATM. Long volatility con un'inclinazione ribassista."},
    },
    "6. Butterfly & Iron Fly": {
        "Long Call Butterfly": {"legs": [{"type": "call", "direction": "long", "strike_offset": -10, "ratio": 1}, {"type": "call", "direction": "short", "ratio": 2}, {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1}], "description": "1 long, 2 short, 1 long. Neutrale, a basso costo, short volatility."},
        "Long Put Butterfly": {"legs": [{"type": "put", "direction": "long", "strike_offset": 10, "ratio": 1}, {"type": "put", "direction": "short", "ratio": 2}, {"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1}], "description": "Equivalente alla Call Butterfly ma costruita con le put."},
        "Iron Butterfly (Short)": {"legs": [{"type": "call", "direction": "short", "ratio": 1}, {"type": "put", "direction": "short", "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1}, {"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1}], "description": "Short Straddle ATM + Long Strangle OTM. Credit, short volatility."},
        "Broken-Wing Call Butterfly": {"legs": [{"type": "call", "direction": "long", "strike_offset": -15, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": -5, "ratio": 2}, {"type": "call", "direction": "long", "strike_offset": 0, "ratio": 1}], "description": "Farfalla con ali asimmetriche per introdurre un'inclinazione direzionale."},
    },
    "7. Condor & Iron Condor": {
        "Long Call Condor": {"legs": [{"type": "call", "direction": "long", "strike_offset": -15, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": -5, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 15, "ratio": 1}], "description": "Bull Call Spread + Bear Call Spread. Debit, long volatility a range."},
        "Iron Condor (Short)": {"legs": [{"type": "put", "direction": "long", "strike_offset": -15, "ratio": 1}, {"type": "put", "direction": "short", "strike_offset": -5, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 15, "ratio": 1}], "description": "Bull Put Spread + Bear Call Spread. Credit, short volatility a range."},
        "Broken-Wing Iron Condor": {"legs": [{"type": "put", "direction": "long", "strike_offset": -20, "ratio": 1}, {"type": "put", "direction": "short", "strike_offset": -10, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1}], "description": "Ali di ampiezza diversa per avere un'inclinazione direzionale."},
    },
    "8. Strutture Complesse": {
        "Jade Lizard": {"legs": [{"type": "put", "direction": "short", "strike_offset": -10, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 15, "ratio": 1}], "description": "Short Put + Bear Call Spread. Obiettivo: rischio zero sul lato rialzista."},
        "Risk Reversal": {"legs": [{"type": "put", "direction": "short", "strike_offset": -10, "ratio": 1}, {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1}], "description": "Short Put OTM + Long Call OTM. Simula una posizione long sul sottostante."},
        "Box Spread": {"legs": [{"type": "call", "direction": "long", "strike_offset": -5, "ratio": 1}, {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1}, {"type": "put", "direction": "short", "strike_offset": -5, "ratio": 1}, {"type": "put", "direction": "long", "strike_offset": 5, "ratio": 1}], "description": "Bull Call Spread + Bear Put Spread. Strategia di arbitraggio, il P/L è una linea piatta."},
    }
}
