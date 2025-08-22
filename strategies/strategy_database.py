# Contiene la definizione strutturata di ogni strategia di opzioni.
# Questo dizionario è il "cervello" che alimenta l'applicazione.

STRATEGY_DATABASE = {
    "Long Call": {
        "legs": [
            {"type": "call", "direction": "long", "ratio": 1},
        ],
        "description": "Acquisto di un'opzione Call. Rialzista, rischio limitato, profitto illimitato."
    },
    "Short Call": {
        "legs": [
            {"type": "call", "direction": "short", "ratio": 1},
        ],
        "description": "Vendita di un'opzione Call. Ribassista/Laterale, profitto limitato, rischio illimitato."
    },
    "Long Put": {
        "legs": [
            {"type": "put", "direction": "long", "ratio": 1},
        ],
        "description": "Acquisto di un'opzione Put. Ribassista, rischio limitato, profitto elevato."
    },
    "Short Put": {
        "legs": [
            {"type": "put", "direction": "short", "ratio": 1},
        ],
        "description": "Vendita di un'opzione Put. Rialzista/Laterale, profitto limitato, rischio elevato."
    },
    "Bull Call Spread": {
        "legs": [
            {"type": "call", "direction": "long", "strike_offset": -5, "ratio": 1},
            {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1},
        ],
        "description": "Strategia rialzista a rischio e rendimento definiti (debit spread)."
    },
    "Bear Put Spread": {
        "legs": [
            {"type": "put", "direction": "long", "strike_offset": 5, "ratio": 1},
            {"type": "put", "direction": "short", "strike_offset": -5, "ratio": 1},
        ],
        "description": "Strategia ribassista a rischio e rendimento definiti (debit spread)."
    },
    "Short Iron Condor": {
        "legs": [
            {"type": "put", "direction": "long", "strike_offset": -15, "ratio": 1},
            {"type": "put", "direction": "short", "strike_offset": -5, "ratio": 1},
            {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1},
            {"type": "call", "direction": "long", "strike_offset": 15, "ratio": 1},
        ],
        "description": "Strategia laterale (short volatility) a rischio e rendimento definiti (credit spread)."
    },
}
