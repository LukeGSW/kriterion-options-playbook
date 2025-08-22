STRATEGY_DATABASE = {
    # 1) Posizioni base & sintetiche
    "1. Posizioni Base & Sintetiche": {
        "Long Stock": {
            "legs": [{"type": "stock", "direction": "long", "ratio": 1}],
            "description": "Acquisto di 100 azioni. Rialzista, Delta ~+100."
        },
        "Short Stock": {
            "legs": [{"type": "stock", "direction": "short", "ratio": 1}],
            "description": "Vendita allo scoperto di 100 azioni. Ribassista, Delta ~-100."
        },
        "Long Call": {
            "legs": [{"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"}],
            "description": "Acquisto di Call. Rialzista, rischio limitato."
        },
        "Short Call": {
            "legs": [{"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"}],
            "description": "Vendita di Call. Ribassista/laterale, rischio teorico illimitato."
        },
        "Long Put": {
            "legs": [{"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}],
            "description": "Acquisto di Put. Ribassista, rischio limitato."
        },
        "Short Put": {
            "legs": [{"type": "put", "direction": "short", "ratio": 1, "moneyness": "OTM"}],
            "description": "Vendita di Put (nuda). Rialzista/laterale."
        },
        "Synthetic Long Stock": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long Call + Short Put (stesso K/scadenza). Replica long sottostante."
        },
        "Synthetic Short Stock": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Short Call + Long Put. Replica short sottostante."
        },
        "Synthetic Long Call": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long Stock + Long Put ≈ Long Call + bond. Rialzista convessa."
        },
        "Synthetic Long Put": {
            "legs": [
                {"type": "stock", "direction": "short", "ratio": 1},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Short Stock + Long Call. Ribassista convessa."
        },
        "Combo (Risk Reversal Bull)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Short Put OTM + Long Call OTM. Bias rialzista."
        },
        "Combo (Risk Reversal Bear)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Short Call OTM + Long Put OTM. Bias ribassista."
        },
    },

    # 2) Covered / Protective / Income
    "2. Covered & Protective": {
        "Covered Call": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Long Stock + Short Call OTM. Income, cap sul rialzo."
        },
        "Protective Put (Married Put)": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Long Stock + Long Put OTM. Assicurazione downside."
        },
        "Collar": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Long Stock + Put OTM + Short Call OTM. Protezione con cap."
        },
        "Zero-Cost Collar / Fence": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -k} for k in []
            ],
            "description": "Come Collar, calibrato per costo netto ≈ 0.",
            "note": "Imposta strike per credito-debito ~0; rappresentazione logica (stesso schema del Collar)."
        },
        "Covered Put": {
            "legs": [
                {"type": "stock", "direction": "short", "ratio": 1},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Short Stock + Short Put. Income con bias ribassista."
        },
        "Cash-Secured Put": {
            "legs": [{"type": "put", "direction": "short", "ratio": 1, "moneyness": "OTM"}],
            "description": "Short Put coperta da cassa (CSP). Ingresso a sconto."
        },
        "Wheel (CSP → CC)": {
            "legs": [{"type": "put", "direction": "short", "ratio": 1, "moneyness": "OTM"}],
            "sequence": [
                "Step 1: Vendi Put OTM (CSP).",
                "Step 2: Se assegnato → diventi Long Stock.",
                "Step 3: Vendi Covered Call OTM ricorrente."
            ],
            "description": "Flusso operativo di income ricorrente."
        },
        "Poor Man’s Covered Call (PMCC)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ITM", "expiry_offset": +6},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "OTM", "expiry_offset": +1}
            ],
            "description": "Long Call LEAPS ITM + Short Call front. Replica CC con minor capitale."
        },
        "Covered Combo": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long Stock + Short Straddle/Strangle. Gestione attiva del delta."
        },
    },

    # 3) Vertical Spreads
    "3. Vertical Spreads": {
        "Bull Call Spread (Debit)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5}
            ],
            "description": "Rialzista, rischio/rendimento definiti."
        },
        "Bear Call Spread (Credit)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +5}
            ],
            "description": "Ribassista/neutral, credit."
        },
        "Bull Put Spread (Credit)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -5}
            ],
            "description": "Rialzista/neutral, credit."
        },
        "Bear Put Spread (Debit)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": +5},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5}
            ],
            "description": "Ribassista, debit."
        },
        "Wide Vertical (Call/Put)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Vertical con ali più lontane (ampiezza maggiore).",
            "note": "Usa 'type' put per variante ribassista simmetrica."
        },
        "Narrow Vertical (Call/Put)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -2},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +2}
            ],
            "description": "Vertical stretto; minor costo/minor credito."
        },
        "Back-to-Back Verticals (Condor-like)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Catena di vertical per sagomare payoff (equivalente a Condor debit)."
        },
    },

    # 4) Ratio & Backspreads
    "4. Ratio & Backspreads": {
        "Call Ratio Spread (Front)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": +5}
            ],
            "description": "Short vol direzionale su call-side."
        },
        "Call Ratio Backspread": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": +5}
            ],
            "description": "Rialzista e long volatility."
        },
        "Put Ratio Backspread": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -5}
            ],
            "description": "Ribassista e long volatility."
        },
        "Front Spread (Call)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": +10}
            ],
            "description": "Long 1 + Short 2 sullo stesso lato; short vol direzionale."
        },
        "Front Spread (Put)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 2, "strike_offset": -10}
            ],
            "description": "Versione put; short vol direzionale."
        },
        "Reverse Ratio (Call)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": +10}
            ],
            "description": "Inversione del front spread; spesso debit, long tail."
        },
        "Reverse Ratio (Put)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -10}
            ],
            "description": "Inversione lato put; tail risk controllata."
        },
        "Ratio Diagonal (Call)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": +10, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Rapporto + scadenze diverse (term/vega play)."
        },
        "Ratio Diagonal (Put)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -10, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Rapporto diagonale lato put."
        },
    },

    # 5) Volatility (Straddle/Strangle) & varianti
    "5. Volatility (Straddle/Strangle)": {
        "Long Straddle": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long vol puro su ATM."
        },
        "Short Straddle": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Short vol; massimo theta."
        },
        "Long Strangle": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Long vol OTM più economico."
        },
        "Short Strangle": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Short vol con BE più ampi."
        },
        "Guts (ITM Strangle) Long": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ITM"},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ITM"}
            ],
            "description": "Strangle ITM; premio alto, sensibilità elevata."
        },
        "Guts (ITM Strangle) Short": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ITM"},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ITM"}
            ],
            "description": "Versione short; rischio elevato."
        },
        "Strip": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 2, "moneyness": "ATM"}
            ],
            "description": "Long vol con bias ribassista."
        },
        "Strap": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long vol con bias rialzista."
        },
        "Ratio Straddle": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Straddle non 1:1 (generalizzabile)."
        },
        "Ratio Strangle": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": +10}
            ],
            "description": "Strangle non 1:1."
        },
        "Joker / Batman": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": +15}
            ],
            "description": "Doppia farfalla/straddle sagomato intorno all’ATM (naming informale)."
        },
    },

    # 6) Butterfly & Iron Fly
    "6. Butterfly & Iron Fly": {
        "Long Call Butterfly (1:-2:1)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 2, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Neutrale, debit, short vol intorno al centro."
        },
        "Long Put Butterfly (1:-2:1)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "short", "ratio": 2, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Neutrale, debit."
        },
        "Iron Butterfly (Short)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Short straddle + ali OTM. Credit, short vol."
        },
        "Iron Butterfly (Long)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Debit, long vol su centro."
        },
        "Broken-Wing Call Butterfly": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 0}
            ],
            "description": "Ali asimmetriche per inclinazione direzionale."
        },
        "Broken-Wing Put Butterfly": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": +15},
                {"type": "put", "direction": "short", "ratio": 2, "strike_offset": +5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 0}
            ],
            "description": "Versione BWB lato put."
        },
        "Skip-Strike Butterfly": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +20}
            ],
            "description": "Si salta uno strike per asimmetria intrinseca."
        },
        "Unbalanced Butterfly (2:-3:1)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 3, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Quantità non 1:-2:1 per drift di delta/theta."
        },
        "Unbalanced Skip-Strike Butterfly": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": +10},
                {"type": "put", "direction": "short", "ratio": 3, "strike_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -20}
            ],
            "description": "Ala saltata + quantità sbilanciate."
        },
        "Christmas-Tree Butterfly": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 3, "strike_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Farfalla a 'scala' con step non equidistanti."
        },
        "Condor-Fly / Fly annidata": {
            "legs": [],
            "description": "Due farfalle contigue/sovrapposte per plateau più largo.",
            "note": "Rappresentare come somma di due farfalle con centri diversi."
        },
        "Rhino (Put BWB Theta+)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": +30},
                {"type": "put", "direction": "short", "ratio": 3, "strike_offset": +10},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 0}
            ],
            "description": "BWB lato put, theta-positive con rischio di coda controllato."
        },
    },

    # 7) Condor & Iron Condor
    "7. Condor & Iron Condor": {
        "Long Call Condor (Debit)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Debit, long vol a range stretto."
        },
        "Long Put Condor (Debit)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": +15},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15}
            ],
            "description": "Debit, neutrale."
        },
        "Iron Condor (Short)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Credit, short vol a range."
        },
        "Iron Condor (Long)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -15},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Debit, long vol."
        },
        "Broken-Wing Iron Condor": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -20},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Ali asimmetriche per inclinare il rischio."
        },
        "Unbalanced Iron Condor": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "put", "direction": "short", "ratio": 2, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Quantità diverse per target di delta."
        },
        "Albatross (Wide IC)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -60},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -30},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +30},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +60}
            ],
            "description": "IC a larghezza molto ampia."
        },
        "Double Iron Condor": {
            "legs": [],
            "description": "Due IC a centri diversi per range multipli.",
            "note": "Rappresenta come somma di due set IC con strike_offset differenti."
        },
    },

    # 8) Calendari, Diagonali & Time Structures
    "8. Calendari, Diagonali & Time": {
        "Call Calendar": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Stesso strike, scadenze diverse; long vol di calendario."
        },
        "Put Calendar": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Analogo lato put."
        },
        "Double Calendar (Time Iron Condor)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10, "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10, "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10, "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Calendario su entrambe le ali; profilo IC nel tempo."
        },
        "Calendar Strangle": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10, "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10, "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10, "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "OTM calendar su entrambi i lati."
        },
        "Calendar Butterfly (Time Fly)": {
            "legs": [],
            "description": "Più calendari concentrati sul centro per picco di vega.",
            "note": "Implementa come somma di calendari con strike centrali."
        },
        "Diagonal Call (Debit)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5, "expiry": "far", "expiry_offset": +3},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5, "expiry": "near", "expiry_offset": +1}
            ],
            "description": "Strike diversi + scadenze diverse."
        },
        "Diagonal Put (Debit)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": +5, "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": +1}
            ],
            "description": "Analogo lato put."
        },
        "Diagonal Call (Credit)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +5, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Versione credit."
        },
        "Diagonal Put (Credit)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": +5, "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -5, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Versione credit lato put."
        },
        "Double Diagonal": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5, "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15, "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Diagonale call + diagonale put; profilo IC nel tempo."
        },
        "Diagonal Condor": {
            "legs": [],
            "description": "Quattro gambe diagonali per sagomare P/L temporale.",
            "note": "Somma di due diagonali per lato call/put con strike/tenor differenziati."
        },
    },

    # 9) Lizards, Seagull, Reversal & affini
    "9. Lizard, Seagull, Reversal & Affini": {
        "Jade Lizard": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Short Put + Call Spread. Obiettivo: zero rischio a rialzo se credito ≥ larghezza call-spread."
        },
        "Reverse Jade Lizard": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15}
            ],
            "description": "Speculare, rischio lato ribasso mitigato dalla put long."
        },
        "Big Lizard": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +25}
            ],
            "description": "Jade con call-spread più largo o credito più alto."
        },
        "Seagull (Bull Capped)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15}
            ],
            "description": "Risk Reversal + opzione aggiuntiva per cap del lato aperto (bull)."
        },
        "Seagull (Bear Capped)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15}
            ],
            "description": "Versione bear; cap del lato aperto."
        },
        "Risk Reversal (Bull)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10}
            ],
            "description": "RR puro lato bull."
        },
        "Risk Reversal (Bear)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "RR puro lato bear."
        },
        "Fence": {
            "legs": [],
            "description": "Sinonimo pratico di collar/RR a costo prossimo allo zero.",
            "note": "Vedi Zero-Cost Collar."
        },
    },

    # 10) Ladder / Scala / Alberi
    "10. Ladder / Scala / Alberi": {
        "Call Ladder (1:-1:-1)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +20}
            ],
            "description": "Acquisto 1 e vendita multipla su strike superiori."
        },
        "Put Ladder (1:-1:-1)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -20}
            ],
            "description": "Analogo lato put."
        },
        "Christmas Tree (Call 1×3×2)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 3, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": +15}
            ],
            "description": "Struttura a scalini con quantità 1×3×2."
        },
        "Christmas Tree (Put 1×3×2)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": +10},
                {"type": "put", "direction": "short", "ratio": 3, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -15}
            ],
            "description": "Versione put."
        },
        "Backspread Ladder": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": +10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +20}
            ],
            "description": "Combinazione di backspread su più livelli per code."
        },
    },

    # 11) Arbitraggio, parità e carry
    "11. Arbitraggio, Parità & Carry": {
        "Box Spread (Call+Put Box)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": +5}
            ],
            "description": "Verticale call + verticale put che replica un bond (carry/arb)."
        },
        "Conversion": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Lock-in del carry tramite parità put-call."
        },
        "Reverse Conversion (Reversal)": {
            "legs": [
                {"type": "stock", "direction": "short", "ratio": 1},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Carry inverso (short carry)."
        },
        "Jelly Roll": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": +3},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1}
            ],
            "description": "Call calendar + Put calendar (stesso strike) per rollare il forward/carry."
        },
        "Split-Strike Conversion": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10}
            ],
            "description": "Variante di collar con strike asimmetrici (hedge + income)."
        },
    },

    # 12) Strutture “evento” e vol-skew specialistiche
    "12. Strutture Evento & Vol-Skew": {
        "Iron Fly (Short/Long)": {
            "legs": [],
            "description": "Vedi sezione 6; spesso utilizzata per earnings/eventi.",
            "note": "Short = credit (short vol); Long = debit (long vol)."
        },
        "Calendar su Straddle (ATM)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Time-spread centrato su ATM per giocare il vega timing."
        },
        "Calendar su Strangle (OTM)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +10, "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +10, "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10, "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Time-spread OTM su entrambe le ali."
        },
        "Diagonal Strangle": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": +5, "expiry": "near", "expiry_offset": +1},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": +15, "expiry": "far", "expiry_offset": +3},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": +1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15, "expiry": "far", "expiry_offset": +3}
            ],
            "description": "Diagonale su entrambe le ali per skew e term-structure."
        },
        "Butterfly di Calendario (Stretta/Larga)": {
            "legs": [],
            "description": "Time-fly concentrata o ampia su IV term.",
            "note": "Somma di più calendari con pesi su strike adiacenti."
        },
        "Condor Time-Spread": {
            "legs": [],
            "description": "Doppi calendari con plateau centrale tipo condor.",
            "note": "Vedi Double Calendar; varia ampiezza/tenor."
        },
        "Gamma-Scalping (con Long Options)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Metodo di gestione delta intraday; non è struttura fissa.",
            "note": "Tipicamente si parte da Long Straddle/Strangle e si fa re-hedge del delta."
        },
    },

    # 13) Varianti operative e nominazioni di bottega
    "13. Varianti Operative & Nominazioni": {
        "Split/Shifted Butterflies": {
            "legs": [],
            "description": "Farfalle non centrate (OTM) per drift di delta.",
            "note": "Sposta lo strike centrale rispetto all’ATM."
        },
        "Symmetric/Asymmetric Condors": {
            "legs": [],
            "description": "IC con ali/crediti diversi per skew.",
            "note": "Regola larghezza ali e credito tra i lati."
        },
        "Iron Albatross (Very Wide IC)": {
            "legs": [],
            "description": "Vedi Albatross (Wide IC) nella sezione 7.",
            "note": "Naming alternativo usato in pratica."
        },
        "Fly-in-Fly (Nested)": {
            "legs": [],
            "description": "Farfalla dentro farfalla per picco theta localizzato.",
            "note": "Somma di farfalle su strike vicini."
        },
        "Double Fly": {
            "legs": [],
            "description": "Due farfalle su strike distinti per doppio picco.",
            "note": "Combinazione di fly ITM/OTM o ±ΔK."
        },
        "Calendar+Diagonal Mix": {
            "legs": [],
            "description": "Ibridi per plasmare curva T+ e vega.",
            "note": "Combina calendario su un lato e diagonale sull’altro."
        },
    },
}
