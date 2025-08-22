# Contiene la definizione strutturata di ogni strategia di opzioni.
# La struttura è un dizionario di dizionari: {categoria: {strategia: dettagli}}.

STRATEGY_DATABASE = {
    "1. Posizioni Base & Sintetiche": {
        "Long Call": {
            "legs": [{"type": "call", "direction": "long", "ratio": 1}],
            "description": "Acquisto di un'opzione Call. Rialzista, rischio limitato, profitto illimitato."
        },
        "Short Call": {
            "legs": [{"type": "call", "direction": "short", "ratio": 1}],
            "description": "Vendita di un'opzione Call. Ribassista/Laterale, profitto limitato, rischio illimitato."
        },
        "Long Put": {
            "legs": [{"type": "put", "direction": "long", "ratio": 1}],
            "description": "Acquisto di un'opzione Put. Ribassista, rischio limitato, profitto elevato."
        },
        "Short Put": {
            "legs": [{"type": "put", "direction": "short", "ratio": 1}],
            "description": "Vendita di un'opzione Put. Rialzista/Laterale, profitto limitato, rischio elevato."
        },
        "Synthetic Long Stock": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "short", "ratio": 1}
            ],
            "description": "Long Call + Short Put. Replica un'esposizione long sul sottostante."
        }
    },
    "2. Covered & Protective": {
        "Covered Call": {
            "legs": [
                # Per ora simuliamo solo le gambe opzionarie
                {"type": "call", "direction": "short", "ratio": 1}
            ],
            "description": "Short Call contro 100 azioni del sottostante. Strategia di income."
        },
        "Protective Put": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1}
            ],
            "description": "Long Put per proteggere 100 azioni del sottostante. Limita il rischio al ribasso."
        },
        "Collar": {
            "legs": [
                {"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1},
                {"type": "call", "direction": "short", "strike_offset": 10, "ratio": 1}
            ],
            "description": "Long Put OTM + Short Call OTM contro 100 azioni. Protezione a costo zero o ridotto."
        }
    },
    "3. Vertical Spreads": {
        "Bull Call Spread": {
            "legs": [
                {"type": "call", "direction": "long", "strike_offset": -5, "ratio": 1},
                {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1}
            ],
            "description": "Strategia rialzista a rischio e rendimento definiti (debit spread)."
        },
        "Bear Call Spread": {
            "legs": [
                {"type": "call", "direction": "short", "strike_offset": -5, "ratio": 1},
                {"type": "call", "direction": "long", "strike_offset": 5, "ratio": 1}
            ],
            "description": "Strategia ribassista/laterale a rischio e rendimento definiti (credit spread)."
        },
        "Bull Put Spread": {
            "legs": [
                {"type": "put", "direction": "short", "strike_offset": 5, "ratio": 1},
                {"type": "put", "direction": "long", "strike_offset": -5, "ratio": 1}
            ],
            "description": "Strategia rialzista/laterale a rischio e rendimento definiti (credit spread)."
        },
        "Bear Put Spread": {
            "legs": [
                {"type": "put", "direction": "long", "strike_offset": 5, "ratio": 1},
                {"type": "put", "direction": "short", "strike_offset": -5, "ratio": 1}
            ],
            "description": "Strategia ribassista a rischio e rendimento definiti (debit spread)."
        }
    },
    "4. Ratio & Backspreads": {
        "Call Ratio Backspread": {
            "legs": [
                {"type": "call", "direction": "short", "strike_offset": -5, "ratio": 1},
                {"type": "call", "direction": "long", "strike_offset": 5, "ratio": 2}
            ],
            "description": "Short 1 Call + Long 2 Call OTM. Rialzista e long volatility."
        },
        "Put Ratio Backspread": {
            "legs": [
                {"type": "put", "direction": "short", "strike_offset": 5, "ratio": 1},
                {"type": "put", "direction": "long", "strike_offset": -5, "ratio": 2}
            ],
            "description": "Short 1 Put + Long 2 Put OTM. Ribassista e long volatility."
        }
    },
    "5. Straddle & Strangle": {
        "Long Straddle": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1}
            ],
            "description": "Long Call ATM + Long Put ATM. Long volatility puro."
        },
        "Short Straddle": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1},
                {"type": "put", "direction": "short", "ratio": 1}
            ],
            "description": "Short Call ATM + Short Put ATM. Short volatility, massimo incasso di theta."
        },
        "Long Strangle": {
            "legs": [
                {"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1},
                {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1}
            ],
            "description": "Long Put OTM + Long Call OTM. Long volatility, più economico di uno straddle."
        },
        "Short Strangle": {
            "legs": [
                {"type": "put", "direction": "short", "strike_offset": -10, "ratio": 1},
                {"type": "call", "direction": "short", "strike_offset": 10, "ratio": 1}
            ],
            "description": "Short Put OTM + Short Call OTM. Short volatility con breakeven ampi."
        }
    },
    "6. Butterfly & Iron Fly": {
        "Long Call Butterfly": {
            "legs": [
                {"type": "call", "direction": "long", "strike_offset": -10, "ratio": 1},
                {"type": "call", "direction": "short", "ratio": 2},
                {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1}
            ],
            "description": "1 long call, 2 short call ATM, 1 long call. Neutrale, a basso costo (debit)."
        },
        "Iron Butterfly": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1},
                {"type": "put", "direction": "short", "ratio": 1},
                {"type": "call", "direction": "long", "strike_offset": 10, "ratio": 1},
                {"type": "put", "direction": "long", "strike_offset": -10, "ratio": 1}
            ],
            "description": "Short Straddle ATM + Long Strangle OTM. Credit, short volatility."
        }
    },
    "7. Condor & Iron Condor": {
        "Iron Condor": {
            "legs": [
                {"type": "put", "direction": "long", "strike_offset": -15, "ratio": 1},
                {"type": "put", "direction": "short", "strike_offset": -5, "ratio": 1},
                {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1},
                {"type": "call", "direction": "long", "strike_offset": 15, "ratio": 1}
            ],
            "description": "Bull Put Spread + Bear Call Spread. Credit, short volatility a range."
        },
        "Long Call Condor": {
            "legs": [
                {"type": "call", "direction": "long", "strike_offset": -15, "ratio": 1},
                {"type": "call", "direction": "short", "strike_offset": -5, "ratio": 1},
                {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1},
                {"type": "call", "direction": "long", "strike_offset": 15, "ratio": 1}
            ],
            "description": "Due vertical spread (un bull e un bear). Debit, long volatility a range."
        }
    },
    "8. Calendari & Diagonali": {
        "Calendar Spread": {
            "legs": [
                # La logica attuale non supporta scadenze diverse, è una simulazione
            ],
            "description": "Short opzione front-month + Long opzione back-month. Long vega, long theta. (SIMULAZIONE NON FUNZIONANTE)"
        },
        "Diagonal Spread": {
            "legs": [
                # La logica attuale non supporta scadenze diverse, è una simulazione
            ],
            "description": "Come un calendar, ma con strike diversi. (SIMULAZIONE NON FUNZIONANTE)"
        }
    },
    "9. Lizards & Seagulls": {
        "Jade Lizard": {
            "legs": [
                {"type": "put", "direction": "short", "strike_offset": -10, "ratio": 1},
                {"type": "call", "direction": "short", "strike_offset": 5, "ratio": 1},
                {"type": "call", "direction": "long", "strike_offset": 15, "ratio": 1}
            ],
            "description": "Short Put + Bear Call Spread. Obiettivo: rischio zero sul lato rialzista."
        }
    },
    # Categorie da 10 a 13 sono segnaposto, la loro logica è spesso troppo complessa per il motore attuale
    "10. Ladder & Alberi": {},
    "11. Arbitraggio & Parità": {},
    "12. Strutture Evento": {},
    "13. Varianti Operative": {}
}
