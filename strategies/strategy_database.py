STRATEGY_DATABASE = {
    # 1) Posizioni base & sintetiche
    "1. Posizioni Base & Sintetiche": {
        "Long Stock": {
            "legs": [{"type": "stock", "direction": "long", "ratio": 1}],
            "description": "Acquisto di 100 azioni. Rialzista, Delta ~+100.",
            "analysis": {
                "when_to_use": "Quando si ha una visione rialzista a lungo termine su un titolo e si desidera una partecipazione diretta nell'azienda.",
                "market_conditions": {
                    "optimal": "📈 Mercato rialzista (trend following).",
                    "poor": "📉 Mercato ribassista o laterale (costo opportunità)."
                },
                "peculiarities": "Esposizione lineare al movimento del prezzo. Delta costante di +100. Tutte le altre greche sono zero. Rischio di perdita teoricamente limitato al capitale investito."
            }
        },
        "Short Stock": {
            "legs": [{"type": "stock", "direction": "short", "ratio": 1}],
            "description": "Vendita allo scoperto di 100 azioni. Ribassista, Delta ~-100.",
            "analysis": {
                "when_to_use": "Quando si ha una forte convinzione ribassista su un titolo.",
                "market_conditions": {
                    "optimal": "📉 Mercato ribassista (trend following).",
                    "poor": "📈 Mercato rialzista (rischio teoricamente illimitato)."
                },
                "peculiarities": "Esposizione lineare inversa. Delta costante di -100. Rischio teoricamente illimitato poiché il prezzo di un'azione può salire all'infinito."
            }
        },
        "Long Call": {
            "legs": [{"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"}],
            "description": "Acquisto di Call. Rialzista, rischio limitato.",
            "analysis": {
                "when_to_use": "Quando si ha una forte convinzione rialzista su un titolo e si desidera un'esposizione con leva finanziaria e un rischio definito e limitato al premio pagato.",
                "market_conditions": {
                    "optimal": "📈 Mercato fortemente direzionale al rialzo (trend/momentum). Volatilità implicita (IV) bassa e in aumento. Utile prima di un evento catalizzatore atteso (es. earnings) con aspettative positive.",
                    "poor": "📉 Mercato laterale o ribassista. La volatilità implicita (IV) molto alta rende i premi costosi (vega risk). Poco tempo alla scadenza accelera il decadimento temporale (theta risk)."
                },
                "peculiarities": "È una delle strategie più semplici con un profilo di rischio/rendimento asimmetrico. Le greche principali sono **Delta positivo** (guadagna se il prezzo sale), **Vega positivo** (guadagna se la IV sale) e **Theta negativo** (perde valore ogni giorno che passa)."
            }
        },
        "Short Call": {
            "legs": [{"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"}],
            "description": "Vendita di Call. Ribassista/laterale, rischio teorico illimitato.",
            "analysis": {
                "when_to_use": "Per generare income quando si ha una visione neutrale, leggermente ribassista o si crede che il titolo non supererà una certa soglia (lo strike) entro la scadenza.",
                "market_conditions": {
                    "optimal": "횡 Mercato laterale o leggermente ribassista. Volatilità implicita (IV) alta e in diminuzione (vega crush).",
                    "poor": "📈 Mercato fortemente rialzista. Un aumento della volatilità implicita è dannoso."
                },
                "peculiarities": "Strategia a probabilità di profitto alta ma con rischio illimitato e profitto limitato. Il **Theta è positivo** (il tempo è a favore del venditore). Il **Delta è negativo** e il **Vega è negativo**."
            }
        },
        "Long Put": {
            "legs": [{"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}],
            "description": "Acquisto di Put. Ribassista, rischio limitato.",
            "analysis": {
                "when_to_use": "Quando si ha una forte convinzione ribassista o si desidera acquistare un'assicurazione contro un calo del mercato o di un singolo titolo. Rischio limitato al premio pagato.",
                "market_conditions": {
                    "optimal": "📉 Mercato fortemente direzionale al ribasso. Volatilità implicita (IV) bassa e in aumento.",
                    "poor": "📈 Mercato laterale o rialzista. IV molto alta rende i premi costosi. Il tempo gioca contro (theta negativo)."
                },
                "peculiarities": "Speculare alla Long Call. Le greche principali sono **Delta negativo**, **Vega positivo** e **Theta negativo**."
            }
        },
        "Short Put": {
            "legs": [{"type": "put", "direction": "short", "ratio": 1, "moneyness": "OTM"}],
            "description": "Vendita di Put (nuda). Rialzista/laterale.",
            "analysis": {
                "when_to_use": "Per generare income quando si ha una visione neutrale o rialzista, o quando si è disposti ad acquistare il sottostante a un prezzo inferiore a quello attuale (lo strike).",
                "market_conditions": {
                    "optimal": "횡 Mercato laterale o rialzista. Volatilità implicita (IV) alta e in diminuzione.",
                    "poor": "📉 Mercato fortemente ribassista. Aumento della volatilità implicita è dannoso."
                },
                "peculiarities": "Spesso usata per iniziare la strategia 'Wheel'. Profilo di rischio/rendimento simile alla Covered Call (parità put-call). **Theta positivo**, **Delta positivo**, **Vega negativo**."
            }
        },
        "Synthetic Long Stock": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long Call + Short Put (stesso K/scadenza). Replica long sottostante.",
            "analysis": {
                "when_to_use": "Per replicare una posizione long sul sottostante con un potenziale minor impiego di capitale iniziale o per ragioni fiscali/di marginazione.",
                "market_conditions": {
                    "optimal": "📈 Mercato rialzista.",
                    "poor": "📉 Mercato ribassista."
                },
                "peculiarities": "Il profilo P/L è quasi identico a quello di 100azioni. Il **Delta della posizione è vicino a +100**. A differenza del possesso diretto di azioni, non si ha diritto a dividendi."
            }
        },
        "Synthetic Short Stock": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Short Call + Long Put. Replica short sottostante.",
             "analysis": {
                "when_to_use": "Per replicare una posizione short sul sottostante, spesso con vantaggi di marginazione rispetto alla vendita allo scoperto tradizionale.",
                "market_conditions": {
                    "optimal": "📉 Mercato ribassista.",
                    "poor": "📈 Mercato rialzista."
                },
                "peculiarities": "Profilo P/L quasi identico a -100 azioni. Il **Delta della posizione è vicino a -100**. Non si devono pagare dividendi come in una normale posizione short."
            }
        },
        "Synthetic Long Call": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long Stock + Long Put ≈ Long Call + bond. Rialzista convessa.",
             "analysis": {
                "when_to_use": "Raramente usata in pratica per creare una call, più che altro una dimostrazione della parità Put-Call. La sua costruzione è identica a una 'Protective Put'.",
                "market_conditions": {
                    "optimal": "📈 Mercato rialzista.",
                    "poor": "📉 Mercato ribassista o laterale."
                },
                "peculiarities": "Dimostra che possedere un'azione e un'assicurazione (put) è finanziariamente equivalente a possedere un biglietto per un rialzo (call) e del contante (il valore attuale dello strike)."
            }
        },
        "Synthetic Long Put": {
            "legs": [
                {"type": "stock", "direction": "short", "ratio": 1},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Short Stock + Long Call. Ribassista convessa.",
            "analysis": {
                "when_to_use": "Dimostrazione della parità Put-Call. Simula una posizione Long Put vendendo allo scoperto il titolo e comprando una call.",
                "market_conditions": {
                    "optimal": "📉 Mercato ribassista.",
                    "poor": "📈 Mercato rialzista o laterale."
                },
                "peculiarities": "Mostra come una scommessa al ribasso con rischio illimitato (short stock) possa essere trasformata in una scommessa a rischio limitato (long put) attraverso l'acquisto di una call."
            }
        },
        "Combo (Risk Reversal Bull)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Short Put OTM + Long Call OTM. Bias rialzista.",
            "analysis": {
                "when_to_use": "Per creare un'esposizione rialzista a basso costo o a credito, finanziando l'acquisto di una call con la vendita di una put. Spesso usata per speculare su un forte movimento al rialzo.",
                "market_conditions": {
                    "optimal": "📈 Mercato fortemente rialzista.",
                    "poor": "📉 Mercato fortemente ribassista (il rischio sulla put venduta è significativo)."
                },
                "peculiarities": "È una versione 'sintetica' di una posizione long sul sottostante ma senza il profilo lineare. È sensibile allo 'skew' di volatilità (la differenza di IV tra call e put OTM)."
            }
        },
        "Combo (Risk Reversal Bear)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Short Call OTM + Long Put OTM. Bias ribassista.",
            "analysis": {
                "when_to_use": "Per creare un'esposizione ribassista a basso costo o a credito, finanziando l'acquisto di una put con la vendita di una call.",
                "market_conditions": {
                    "optimal": "📉 Mercato fortemente ribassista.",
                    "poor": "📈 Mercato fortemente rialzista (rischio illimitato sulla call venduta)."
                },
                "peculiarities": "Speculare alla versione rialzista. Molto comune nel mercato del Forex per strategie di hedging e speculative."
            }
        },
    },

    "2. Covered & Protective": {
        "Covered Call": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Long Stock + Short Call OTM. Income, cap sul rialzo.",
            "analysis": {
                "when_to_use": "Per generare un flusso di cassa (income) da un'azione che si possiede già e su cui si ha una visione neutrale o moderatamente rialzista nel breve termine. Ottima per ridurre la base di costo del proprio investimento.",
                "market_conditions": {
                    "optimal": "횡 Mercato stabile, leggermente rialzista o laterale. Volatilità implicita (IV) elevata permette di vendere call a premi più alti, massimizzando il rendimento.",
                    "poor": "📈 Mercato fortemente rialzista, in quanto il profitto sul sottostante viene 'cappato' dallo strike della call venduta. 📉 Un forte ribasso non viene arginato (la protezione è limitata al premio incassato)."
                },
                "peculiarities": "Trasforma un asset (le azioni) in una 'macchina da rendita'. Non è una strategia per speculare su grandi rialzi. Il suo Delta è inferiore a 100 (quello del solo sottostante) e il suo Theta è positivo, generando profitto dal passare del tempo."
            }
        },
        "Protective Put (Married Put)": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Long Stock + Long Put OTM. Assicurazione downside.",
             "analysis": {
                "when_to_use": "Per proteggere un portafoglio o una singola posizione da un crollo del mercato. Si acquista un'assicurazione sul proprio investimento.",
                "market_conditions": {
                    "optimal": "📈 Mercato rialzista (la put scade senza valore e si beneficia del rialzo del titolo). È 'ottimale' anche in un crollo 📉, perché svolge la sua funzione protettiva.",
                    "poor": "횡 Mercato laterale, dove il costo della put (theta decay) erode i profitti."
                },
                "peculiarities": "Il costo della put (il premio) è il costo dell'assicurazione. Limita la perdita massima a un valore predefinito, ma riduce anche il profitto totale se il mercato sale."
            }
        },
        "Collar": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Long Stock + Put OTM + Short Call OTM. Protezione con cap.",
            "analysis": {
                "when_to_use": "Per proteggere una posizione long (come la Protective Put) ma finanziando l'acquisto della put attraverso la vendita di una call. Si accetta un limite ai profitti in cambio di una protezione a basso costo o a costo zero.",
                "market_conditions": {
                    "optimal": "횡 Mercato laterale o moderatamente rialzista, dove si incassa il theta e si beneficia di un piccolo rialzo fino allo strike della call.",
                    "poor": "📈 Mercato fortemente rialzista (profitti limitati)."
                },
                "peculiarities": "Crea un 'collare' (un range) di possibili P/L. Il rischio e il rendimento sono entrambi limitati. Molto usata da investitori istituzionali e dirigenti con grandi posizioni azionarie."
            }
        },
        "Zero-Cost Collar / Fence": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Come Collar, calibrato per costo netto ≈ 0.",
            "note": "Imposta strike per credito-debito ~0; rappresentazione logica (stesso schema del Collar).",
             "analysis": {
                "when_to_use": "Esattamente come un Collar, ma con una selezione di strike tale per cui il premio ricevuto dalla vendita della call copre quasi perfettamente il costo della put acquistata.",
                "market_conditions": {
                    "optimal": "Simili a quelle del Collar. Particolarmente utile in mercati con uno 'skew' di volatilità favorevole.",
                    "poor": "Simili a quelle del Collar."
                },
                "peculiarities": "L'obiettivo è ottenere una protezione 'gratuita' in cambio della rinuncia a un upside significativo. Il range tra lo strike della put e quello della call è il 'recinto' (fence) entro cui si realizza il risultato."
            }
        },
        "Covered Put": {
            "legs": [
                {"type": "stock", "direction": "short", "ratio": 1},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Short Stock + Short Put. Income con bias ribassista.",
             "analysis": {
                "when_to_use": "L'equivalente ribassista della Covered Call. Si usa quando si ha già una posizione short su un titolo e si vuole generare income da essa, con una visione neutrale o moderatamente ribassista.",
                "market_conditions": {
                    "optimal": "횡 Mercato laterale o leggermente ribassista. IV alta.",
                    "poor": "📈 Mercato fortemente rialzista (la posizione short sul titolo genera perdite illimitate). 📉 Un forte crollo limita i profitti della posizione short."
                },
                "peculiarities": "Meno comune della Covered Call, perché meno investitori mantengono posizioni short a lungo termine. Il profilo di rischio è speculare."
            }
        },
        "Cash-Secured Put": {
            "legs": [{"type": "put", "direction": "short", "ratio": 1, "moneyness": "OTM"}],
            "description": "Short Put coperta da cassa (CSP). Ingresso a sconto.",
             "analysis": {
                "when_to_use": "Vedi 'Short Put'. Il termine 'Cash-Secured' enfatizza la pratica corretta di avere abbastanza liquidità per acquistare le azioni se si viene assegnati.",
                "market_conditions": {
                    "optimal": "Vedi 'Short Put'.",
                    "poor": "Vedi 'Short Put'."
                },
                "peculiarities": "È una strategia di acquisizione di titoli. L'obiettivo non è solo l'income, ma entrare in possesso del titolo a un prezzo più favorevole (strike - premio)."
            }
        },
        "Wheel (CSP → CC)": {
            "legs": [{"type": "put", "direction": "short", "ratio": 1, "moneyness": "OTM"}],
            "sequence": [
                "Step 1: Vendi Put OTM (CSP).",
                "Step 2: Se assegnato → diventi Long Stock.",
                "Step 3: Vendi Covered Call OTM ricorrente."
            ],
            "description": "Flusso operativo di income ricorrente.",
             "analysis": {
                "when_to_use": "Come strategia completa di gestione del portafoglio per generare un reddito costante da un paniere di titoli su cui si ha una visione a lungo termine positiva.",
                "market_conditions": {
                    "optimal": "횡 Mercati laterali o leggermente rialzisti, con buona volatilità implicita.",
                    "poor": "📉 Mercati fortemente ribassisti possono portare ad assegnazioni su titoli che continuano a scendere di valore."
                },
                "peculiarities": "Non è una singola strategia, ma un processo ciclico (una 'ruota'). Richiede una gestione attiva. Il grafico mostra solo il primo passo (vendita della Put)."
            }
        },
        "Poor Man’s Covered Call (PMCC)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ITM", "expiry_offset": 180},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "OTM", "expiry_offset": 0}
            ],
            "description": "Long Call LEAPS ITM + Short Call front. Replica CC con minor capitale.",
            "analysis": {
                "when_to_use": "Per replicare una strategia Covered Call senza dover acquistare le 100 azioni, riducendo drasticamente il capitale richiesto. Si usa una call a lunga scadenza (LEAPS) ITM come surrogato delle azioni.",
                "market_conditions": {
                    "optimal": "Simili alla Covered Call: mercato laterale o moderatamente rialzista.",
                    "poor": "📉 Un forte ribasso può causare perdite significative sulla call LEAPS. 📈 Un forte rialzo è limitato."
                },
                "peculiarities": "È un tipo di spread diagonale. Il profitto deriva dalla differenza nel decadimento temporale (theta) tra la call venduta (scadenza vicina, theta alto) e quella acquistata (scadenza lontana, theta basso)."
            }
        },
        "Covered Combo": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long Stock + Short Straddle/Strangle. Gestione attiva del delta.",
            "analysis": {
                "when_to_use": "Per generare un income aggressivo su una posizione azionaria esistente, quando ci si aspetta che il titolo rimanga estremamente stabile.",
                "market_conditions": {
                    "optimal": "횡 Mercato estremamente laterale (pinning allo strike). IV alta e in calo.",
                    "poor": "📈📉 Qualsiasi movimento significativo in entrambe le direzioni può portare a perdite."
                },
                "peculiarities": "Aggiunge una posizione Short Straddle a 100 azioni. È una strategia ad alto rischio che richiede una gestione molto attiva del delta per rimanere neutrali."
            }
        },
    },

    "3. Vertical Spreads": {
        "Bull Call Spread (Debit)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5}
            ],
            "description": "Rialzista, rischio/rendimento definiti.",
            "analysis": {
                "when_to_use": "Quando si è moderatamente rialzisti e si vuole limitare sia il costo della strategia sia il rischio. Si rinuncia a un profitto illimitato in cambio di un costo d'ingresso inferiore rispetto a una Long Call secca.",
                "market_conditions": {
                    "optimal": "📈 Mercato moderatamente rialzista, con il prezzo che si muove al di sopra dello strike venduto.",
                    "poor": "📉 Mercato ribassista o laterale al di sotto dello strike comprato."
                },
                "peculiarities": "Strategia a debito. Rischio e rendimento massimi sono fissati al momento dell'apertura. Il P/L massimo si raggiunge quando il prezzo del sottostante supera lo strike della call venduta."
            }
        },
        "Bear Call Spread (Credit)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 5}
            ],
            "description": "Ribassista/neutral, credit.",
            "analysis": {
                "when_to_use": "Quando si è neutrali o moderatamente ribassisti. Si incassa un premio (credito) e si profitta se il sottostante rimane al di sotto dello strike venduto.",
                "market_conditions": {
                    "optimal": "횡📉 Mercato laterale o ribassista. IV alta e in calo.",
                    "poor": "📈 Mercato fortemente rialzista, con il prezzo che supera lo strike della call comprata."
                },
                "peculiarities": "Strategia a credito. Il profitto massimo è il premio incassato. Il tempo (Theta positivo) e il calo della volatilità (Vega negativo) sono favorevoli."
            }
        },
        "Bull Put Spread (Credit)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -5}
            ],
            "description": "Rialzista/neutral, credit.",
            "analysis": {
                "when_to_use": "Quando si è neutrali o moderatamente rialzisti. Si scommette che il prezzo del sottostante non scenderà al di sotto di un certo livello (lo strike venduto).",
                "market_conditions": {
                    "optimal": "횡📈 Mercato laterale o rialzista. IV alta e in calo.",
                    "poor": "📉 Mercato fortemente ribassista."
                },
                "peculiarities": "Strategia a credito, il suo profilo di rischio è molto simile a un Bear Call Spread. Il profitto massimo è il premio incassato. Theta e Vega sono alleati."
            }
        },
        "Bear Put Spread (Debit)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 5},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5}
            ],
            "description": "Ribassista, debit.",
            "analysis": {
                "when_to_use": "Quando si è moderatamente ribassisti e si vuole limitare il costo e il rischio rispetto a una Long Put secca.",
                "market_conditions": {
                    "optimal": "📉 Mercato moderatamente ribassista.",
                    "poor": "📈 Mercato rialzista o laterale al di sopra dello strike comprato."
                },
                "peculiarities": "Strategia a debito, speculare al Bull Call Spread. Il P/L massimo si raggiunge quando il prezzo scende al di sotto dello strike della put venduta."
            }
        },
        "Wide Vertical (Call/Put)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Vertical con ali più lontane (ampiezza maggiore).",
            "note": "Usa 'type' put per variante ribassista simmetrica.",
            "analysis": {
                "when_to_use": "Quando si desidera un profilo più direzionale da uno spread. Un'ampiezza maggiore aumenta il profitto potenziale (e il debito/rischio), rendendolo più simile a una long/short call/put secca.",
                "market_conditions": {
                    "optimal": "Mercati con una chiara tendenza attesa.",
                    "poor": "Mercati laterali."
                },
                "peculiarities": "Aumentando la distanza tra gli strike, il Delta della posizione aumenta, così come il costo (se a debito) o il rischio (se a credito)."
            }
        },
        "Narrow Vertical (Call/Put)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -2},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 2}
            ],
            "description": "Vertical stretto; minor costo/minor credito.",
             "analysis": {
                "when_to_use": "Quando si vuole scommettere su un piccolo movimento o semplicemente incassare un premio con un rischio molto contenuto. Spesso usati in strategie ad alta probabilità di successo.",
                "market_conditions": {
                    "optimal": "Mercati poco volatili o con un leggero drift atteso.",
                    "poor": "Mercati molto volatili che possono facilmente superare il range stretto."
                },
                "peculiarities": "Gli spread stretti hanno un Delta più basso e un Theta (se a credito) proporzionalmente più alto rispetto al rischio."
            }
        },
        "Back-to-Back Verticals (Condor-like)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15}
            ],
            "description": "Catena di vertical per sagomare payoff (equivalente a Condor debit).",
            "analysis": {
                "when_to_use": "Vedi 'Long Call Condor'. Questa è solo una costruzione alternativa della stessa strategia, combinando un Bull Call Spread e un Bear Call Spread.",
                "market_conditions": {
                    "optimal": "Vedi 'Long Call Condor'.",
                    "poor": "Vedi 'Long Call Condor'."
                },
                "peculiarities": "Mostra come strategie complesse possano essere scomposte in blocchi più semplici. Utile a livello didattico."
            }
        },
    },

    "4. Ratio & Backspreads": {
        "Call Ratio Spread (Front)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": 5}
            ],
            "description": "Short vol direzionale su call-side.",
            "analysis": {
                "when_to_use": "Quando ci si aspetta che il titolo salga moderatamente, ma non troppo. Si profitta da un piccolo rialzo e dal decadimento temporale delle opzioni vendute in eccesso.",
                "market_conditions": {
                    "optimal": "📈 Mercato moderatamente rialzista. IV alta e in calo.",
                    "poor": "📈 Mercato molto rialzista (la call venduta nuda crea rischio illimitato). 📉 Mercato ribassista."
                },
                "peculiarities": "Spesso impostata a credito. Contiene una componente a rischio illimitato a causa della gamba call venduta 'scoperta' (il rapporto è 1:2)."
            }
        },
        "Call Ratio Backspread": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": 5}
            ],
            "description": "Rialzista e long volatility.",
             "analysis": {
                "when_to_use": "Quando ci si aspetta un forte movimento rialzista e/o un aumento della volatilità. Si sacrifica un profitto in un mercato laterale per un potenziale di guadagno illimitato al rialzo.",
                "market_conditions": {
                    "optimal": "📈 Mercato esplosivo al rialzo. IV bassa e in forte aumento.",
                    "poor": "횡 Mercato laterale tra i due strike (si subisce la perdita massima)."
                },
                "peculiarities": "Spesso impostata a debito zero o a credito. Il profilo P/L è unico: ha un profitto illimitato al rialzo e un profitto limitato se il mercato crolla. La perdita massima è in un punto specifico."
            }
        },
        "Put Ratio Backspread": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -5}
            ],
            "description": "Ribassista e long volatility.",
             "analysis": {
                "when_to_use": "L'esatto opposto del Call Ratio Backspread. Quando ci si aspetta un crollo del mercato e/o un aumento della volatilità.",
                "market_conditions": {
                    "optimal": "📉 Mercato esplosivo al ribasso. IV bassa e in forte aumento.",
                    "poor": "횡 Mercato laterale tra i due strike."
                },
                "peculiarities": "Profilo P/L speculare alla versione con le call. Profitto 'illimitato' al ribasso (fino a zero), profitto limitato al rialzo."
            }
        },
        "Front Spread (Call)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": 10}
            ],
            "description": "Long 1 + Short 2 sullo stesso lato; short vol direzionale.",
            "analysis": {
                "when_to_use": "Vedi 'Call Ratio Spread (Front)'. È un nome alternativo per la stessa struttura.",
                "market_conditions": { "optimal": "Vedi 'Call Ratio Spread (Front)'.", "poor": "Vedi 'Call Ratio Spread (Front)'." },
                "peculiarities": "Vedi 'Call Ratio Spread (Front)'."
            }
        },
        "Front Spread (Put)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 2, "strike_offset": -10}
            ],
            "description": "Versione put; short vol direzionale.",
             "analysis": {
                "when_to_use": "Quando ci si aspetta che il titolo scenda moderatamente, ma non troppo.",
                "market_conditions": { "optimal": "📉 Mercato moderatamente ribassista. IV alta e in calo.", "poor": "📉 Mercato molto ribassista (rischio illimitato). 📈 Mercato rialzista." },
                "peculiarities": "Speculare alla versione call. Rischio illimitato al ribasso."
            }
        },
        "Reverse Ratio (Call)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": 10}
            ],
            "description": "Inversione del front spread; spesso debit, long tail.",
            "analysis": {
                "when_to_use": "Vedi 'Call Ratio Backspread'. È un nome alternativo.",
                "market_conditions": { "optimal": "Vedi 'Call Ratio Backspread'.", "poor": "Vedi 'Call Ratio Backspread'." },
                "peculiarities": "Vedi 'Call Ratio Backspread'."
            }
        },
        "Reverse Ratio (Put)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -10}
            ],
            "description": "Inversione lato put; tail risk controllata.",
            "analysis": {
                "when_to_use": "Vedi 'Put Ratio Backspread'. È un nome alternativo.",
                "market_conditions": { "optimal": "Vedi 'Put Ratio Backspread'.", "poor": "Vedi 'Put Ratio Backspread'." },
                "peculiarities": "Vedi 'Put Ratio Backspread'."
            }
        },
        "Ratio Diagonal (Call)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": 10, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Rapporto + scadenze diverse (term/vega play).",
            "analysis": {
                "when_to_use": "Strategia complessa per sfruttare anomalie nella struttura a termine della volatilità, con una visione direzionale rialzista.",
                "market_conditions": { "optimal": "IV della scadenza lontana sottovalutata rispetto alla vicina; forte movimento rialzista.", "poor": "Crollo della IV a lungo termine, mercato laterale o ribassista." },
                "peculiarities": "Combina elementi di un ratio spread e di un calendar spread. Molto sensibile ai cambiamenti di Vega e della term structure."
            }
        },
        "Ratio Diagonal (Put)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -10, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Rapporto diagonale lato put.",
            "analysis": {
                "when_to_use": "Speculare alla versione call, per sfruttare anomalie nella term structure con una visione ribassista.",
                "market_conditions": { "optimal": "IV della scadenza lontana sottovalutata; forte movimento ribassista.", "poor": "Crollo della IV a lungo termine, mercato laterale o rialzista." },
                "peculiarities": "Profilo di rischio/rendimento complesso, molto dipendente da Vega e Theta."
            }
        },
    },

    "5. Volatility (Straddle/Strangle)": {
        "Long Straddle": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long vol puro su ATM.",
            "analysis": {
                "when_to_use": "Quando ci si aspetta un movimento di prezzo molto forte, ma non si sa in quale direzione. Classica strategia da usare prima di un evento binario (earnings, news).",
                "market_conditions": { "optimal": "IV bassa e in forte aumento. Un grande movimento di prezzo post-evento.", "poor": "IV alta e in calo (vega crush). Mercato che non si muove dopo l'evento (theta decay)." },
                "peculiarities": "Puro gioco sulla volatilità. **Delta vicino a zero**, **Gamma e Vega positivi e massimi**, **Theta negativo e massimo**. Il costo (theta) è molto alto, è una 'lotta contro il tempo'."
            }
        },
        "Short Straddle": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Short vol; massimo theta.",
            "analysis": {
                "when_to_use": "Quando ci si aspetta che il prezzo del sottostante rimanga fermo. Si vende volatilità per incassare il premio.",
                "market_conditions": { "optimal": "IV alta e in calo. Mercato immobile.", "poor": "Qualsiasi movimento di prezzo significativo. Aumento della IV." },
                "peculiarities": "Rischio illimitato su entrambi i lati. **Theta positivo e massimo**, **Gamma e Vega negativi e massimi**. Molto rischiosa se non gestita attivamente."
            }
        },
        "Long Strangle": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Long vol OTM più economico.",
            "analysis": {
                "when_to_use": "Simile al Long Straddle, ma più economico. Richiede un movimento di prezzo ancora più ampio per essere profittevole, ma costa meno.",
                "market_conditions": { "optimal": "Simili al Long Straddle, ma con un movimento di prezzo atteso ancora maggiore.", "poor": "Simili al Long Straddle." },
                "peculiarities": "Minor costo (theta decay più basso) rispetto allo Straddle, ma i breakeven sono più lontani. **Gamma e Vega positivi** (ma inferiori allo Straddle)."
            }
        },
        "Short Strangle": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Short vol con BE più ampi.",
            "analysis": {
                "when_to_use": "Simile allo Short Straddle, ma con un range di profitto più ampio e un credito inferiore. Considerata 'più sicura' dello Straddle.",
                "market_conditions": { "optimal": "IV alta e in calo. Mercato che rimane all'interno degli strike venduti.", "poor": "Un forte movimento che supera uno degli strike." },
                "peculiarities": "Strategia molto popolare per la raccolta di premi. Rischio illimitato. **Theta positivo, Gamma e Vega negativi**."
            }
        },
        "Guts (ITM Strangle) Long": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ITM", "strike_offset": 10},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ITM", "strike_offset": -10}
            ],
            "description": "Strangle ITM; premio alto, sensibilità elevata.",
            "analysis": {
                "when_to_use": "Raramente usata. È una scommessa sulla volatilità che parte già con un valore intrinseco. Richiede un movimento molto rapido per superare il costo elevato.",
                "market_conditions": { "optimal": "Mercato che si muove rapidamente fuori dal range degli strike ITM.", "poor": "Mercato che rimane tra i due strike." },
                "peculiarities": "Costo (debito) molto elevato. Il profilo di P/L è a forma di 'U' rovesciata."
            }
        },
        "Guts (ITM Strangle) Short": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ITM", "strike_offset": 10},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ITM", "strike_offset": -10}
            ],
            "description": "Versione short; rischio elevato.",
            "analysis": {
                "when_to_use": "Strategia estremamente rischiosa, usata quando ci si aspetta che il prezzo rimanga confinato in un range molto stretto tra i due strike ITM.",
                "market_conditions": { "optimal": "Mercato immobile. IV in crollo.", "poor": "Qualsiasi movimento al di fuori del range stretto." },
                "peculiarities": "Credito molto elevato, ma rischio altrettanto elevato. Il P/L è a forma di 'U'."
            }
        },
        "Strip": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 2, "moneyness": "ATM"}
            ],
            "description": "Long vol con bias ribassista.",
            "analysis": {
                "when_to_use": "Simile a un Long Straddle, ma quando si crede che il movimento di prezzo atteso sia più probabilmente al ribasso.",
                "market_conditions": { "optimal": "Grande movimento di prezzo, specialmente al ribasso. IV in aumento.", "poor": "Mercato laterale." },
                "peculiarities": "È uno Straddle sbilanciato (ratio 1:2). Ha un **Delta negativo**, a differenza dello Straddle che è delta-neutral all'inizio."
            }
        },
        "Strap": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Long vol con bias rialzista.",
            "analysis": {
                "when_to_use": "Simile a un Long Straddle, ma quando si crede che il movimento di prezzo atteso sia più probabilmente al rialzo.",
                "market_conditions": { "optimal": "Grande movimento di prezzo, specialmente al rialzo. IV in aumento.", "poor": "Mercato laterale." },
                "peculiarities": "È uno Straddle sbilanciato (ratio 2:1). Ha un **Delta positivo**."
            }
        },
        "Ratio Straddle": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Straddle non 1:1 (generalizzabile).",
            "analysis": {
                "when_to_use": "Vedi 'Strap' o 'Strip'. Il termine è generico per indicare un rapporto non 1:1.",
                "market_conditions": { "optimal": "Dipende dal rapporto scelto.", "poor": "Mercato laterale." },
                "peculiarities": "Permette di inserire un'inclinazione direzionale (un 'bias') in una strategia di volatilità pura."
            }
        },
        "Ratio Strangle": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": 10}
            ],
            "description": "Strangle non 1:1.",
            "analysis": {
                "when_to_use": "Simile a uno Strangle, ma con un'inclinazione direzionale. In questo esempio, si scommette su un movimento più probabile al rialzo.",
                "market_conditions": { "optimal": "Grande movimento di prezzo, specialmente nella direzione del lato con più opzioni. IV in aumento.", "poor": "Mercato laterale." },
                "peculiarities": "Simile a uno Strap/Strip, ma con opzioni OTM, rendendolo più economico ma con breakeven più lontani."
            }
        },
        "Joker / Batman": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": 15}
            ],
            "description": "Doppia farfalla/straddle sagomato intorno all’ATM (naming informale).",
            "analysis": {
                "when_to_use": "Strategia molto complessa per mercati che si prevedono rimanere in un range, ma con la possibilità di un profitto se il movimento è esplosivo. Tenta di avere un P/L a forma di 'M'.",
                "market_conditions": { "optimal": "Mercato che si muove in uno dei due 'picchi' di profitto. IV in calo.", "poor": "Mercato che rimane esattamente al centro o si muove oltre i breakeven esterni." },
                "peculiarities": "È una combinazione di altre strategie, solitamente un M-shape P/L si ottiene combinando un long e un short vertical spread. Il nome 'Batman' deriva dalla forma del grafico P/L."
            }
        },
    },

    "6. Butterfly & Iron Fly": {
        "Long Call Butterfly (1:-2:1)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 2, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Neutrale, debit, short vol intorno al centro.",
            "analysis": {
                "when_to_use": "Quando ci si aspetta che il prezzo del sottostante sia quasi fermo e si trovi esattamente allo strike centrale alla scadenza. È una scommessa sulla stabilità con rischio definito e basso costo.",
                "market_conditions": { "optimal": "Mercato immobile allo strike centrale. IV alta e in calo.", "poor": "Un forte movimento in qualsiasi direzione. Aumento della IV." },
                "peculiarities": "Rischio e costo molto bassi. Il profitto massimo si ha solo in un punto preciso. **Gamma molto negativo** al centro (il P/L cambia rapidamente vicino allo strike), **Theta positivo**."
            }
        },
        "Long Put Butterfly (1:-2:1)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 10},
                {"type": "put", "direction": "short", "ratio": 2, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Neutrale, debit.",
            "analysis": {
                "when_to_use": "Esattamente come la Call Butterfly. La scelta tra put e call può dipendere dallo skew di volatilità o da preferenze di prezzo.",
                "market_conditions": { "optimal": "Vedi Long Call Butterfly.", "poor": "Vedi Long Call Butterfly." },
                "peculiarities": "Grazie alla parità put-call, il profilo di rischio/rendimento è quasi identico alla versione con le call."
            }
        },
        "Iron Butterfly (Short)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Short straddle + ali OTM. Credit, short vol.",
            "analysis": {
                "when_to_use": "Simile a una Long Butterfly, ma viene aperta a credito. Si profitta se il mercato rimane fermo.",
                "market_conditions": { "optimal": "Mercato immobile. IV alta e in calo.", "poor": "Forte movimento direzionale." },
                "peculiarities": "È la combinazione di uno Short Straddle e un Long Strangle. Il profilo P/L è identico a una Long Butterfly, ma essendo a credito, il profitto massimo è il premio incassato."
            }
        },
        "Iron Butterfly (Long)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10}
            ],
            "description": "Debit, long vol su centro.",
            "analysis": {
                "when_to_use": "Raramente usata. È l'inverso di una Iron Butterfly. Si profitta se il mercato si muove molto, simile a un Long Straddle, ma con un costo inferiore e un profitto limitato.",
                "market_conditions": { "optimal": "Forte movimento direzionale. IV in aumento.", "poor": "Mercato immobile." },
                "peculiarities": "È una combinazione di un Long Straddle e uno Short Strangle. Il profilo P/L è quello di un Long Straddle con le 'ali tagliate'."
            }
        },
        "Broken-Wing Call Butterfly": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 0}
            ],
            "description": "Ali asimmetriche per inclinazione direzionale.",
            "analysis": {
                "when_to_use": "Per introdurre un'inclinazione direzionale in una strategia Butterfly. Si sacrifica il profitto (o si aumenta il rischio) su un lato per aumentare il profitto o ridurre il rischio sull'altro.",
                "market_conditions": { "optimal": "Mercato che si muove leggermente nella direzione desiderata.", "poor": "Mercato che si muove nella direzione opposta a quella del 'broken wing'." },
                "peculiarities": "Spostando uno degli strike, si altera la simmetria. Può essere impostata per un piccolo debito, a costo zero, o anche a credito. Molto versatile per la gestione del rischio."
            }
        },
        "Broken-Wing Put Butterfly": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 15},
                {"type": "put", "direction": "short", "ratio": 2, "strike_offset": 5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 0}
            ],
            "description": "Versione BWB lato put.",
            "analysis": {
                "when_to_use": "Speculare alla versione con le call, per introdurre un'inclinazione direzionale ribassista.",
                "market_conditions": { "optimal": "Vedi BWB Call, ma con view ribassista.", "poor": "Vedi BWB Call, ma con view rialzista." },
                "peculiarities": "Stessa logica della BWB Call, ma costruita sul lato delle put."
            }
        },
        "Skip-Strike Butterfly": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 2, "strike_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 20}
            ],
            "description": "Si salta uno strike per asimmetria intrinseca.",
            "analysis": {
                "when_to_use": "Simile a una Broken-Wing, ma si ottiene l'asimmetria allargando una delle ali invece di spostare il centro. Crea un'area di profitto più ampia su un lato.",
                "market_conditions": { "optimal": "Mercato che si muove moderatamente nella direzione dell'ala larga.", "poor": "Mercato che si muove nella direzione dell'ala stretta." },
                "peculiarities": "Il risultato è un profilo di P/L distorto, utile per esprimere view più complesse sulla distribuzione futura dei prezzi."
            }
        },
        "Unbalanced Butterfly (2:-3:1)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 3, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Quantità non 1:-2:1 per drift di delta/theta."
        },
        "Unbalanced Skip-Strike Butterfly": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": 10},
                {"type": "put", "direction": "short", "ratio": 3, "strike_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -20}
            ],
            "description": "Ala saltata + quantità sbilanciate."
        },
        "Christmas-Tree Butterfly": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 3, "strike_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15}
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
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": 30},
                {"type": "put", "direction": "short", "ratio": 3, "strike_offset": 10},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 0}
            ],
            "description": "BWB lato put, theta-positive con rischio di coda controllato."
        },
    },

    "7. Condor & Iron Condor": {
        "Long Call Condor (Debit)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15}
            ],
            "description": "Debit, long vol a range stretto.",
            "analysis": {
                "when_to_use": "Quando ci si aspetta un grande movimento di prezzo, ma si crede che rimarrà confinato tra due estremi. È una scommessa long volatility con profitto limitato.",
                "market_conditions": { "optimal": "Forte movimento di prezzo che rimane all'interno degli strike più esterni. IV in aumento.", "poor": "Mercato immobile tra gli strike centrali." },
                "peculiarities": "È la combinazione di un Bull Call Spread e un Bear Call Spread. Il profilo P/L ha un'area di perdita massima piatta al centro."
            }
        },
        "Long Put Condor (Debit)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 15},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15}
            ],
            "description": "Debit, neutrale.",
            "analysis": {
                "when_to_use": "Identica alla versione con le call.",
                "market_conditions": { "optimal": "Vedi Long Call Condor.", "poor": "Vedi Long Call Condor." },
                "peculiarities": "Profilo di rischio/rendimento quasi identico alla versione call."
            }
        },
        "Iron Condor (Short)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15}
            ],
            "description": "Credit, short vol a range.",
            "analysis": {
                "when_to_use": "Quando ci si aspetta che il prezzo del sottostante rimanga all'interno di un range di prezzo ben definito fino alla scadenza. È una strategia di income che scommette sulla bassa volatilità.",
                "market_conditions": {
                    "optimal": "횡 Mercato laterale e noioso (consolidamento). Volatilità implicita (IV) alta e in diminuzione (vega crush), che permette di vendere premi costosi e vederli sgonfiare.",
                    "poor": "📈📉 Mercato fortemente direzionale in una delle due direzioni. Bassa volatilità implicita (IV) offre premi poco generosi. Rischio maggiore in prossimità della scadenza (gamma risk)."
                },
                "peculiarities": "Rischio e rendimento sono entrambi definiti. È una 'corsa contro il tempo': il **Theta positivo** è il motore del profitto, mentre il **Gamma negativo** è il rischio principale man mano che il prezzo si avvicina agli strike interni. Il **Vega è negativo**."
            }
        },
        "Iron Condor (Long)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -15},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 15}
            ],
            "description": "Debit, long vol.",
            "analysis": {
                "when_to_use": "Vedi Long Call/Put Condor. È la stessa strategia, ma costruita vendendo un Iron Condor invece di comprarlo.",
                "market_conditions": { "optimal": "Vedi Long Call Condor.", "poor": "Vedi Long Call Condor." },
                "peculiarities": "È la combinazione di un Bear Put Spread e un Bull Call Spread."
            }
        },
        "Broken-Wing Iron Condor": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -20},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10}
            ],
            "description": "Ali asimmetriche per inclinare il rischio."
        },
        "Unbalanced Iron Condor": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15},
                {"type": "put", "direction": "short", "ratio": 2, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15}
            ],
            "description": "Quantità diverse per target di delta."
        },
        "Albatross (Wide IC)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -60},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -30},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 30},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 60}
            ],
            "description": "IC a larghezza molto ampia."
        },
        "Double Iron Condor": {
            "legs": [],
            "description": "Due IC a centri diversi per range multipli.",
            "note": "Rappresenta come somma di due set IC con strike_offset differenti."
        },
    },

    "8. Calendari, Diagonali & Time": {
        "Call Calendar": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Stesso strike, scadenze diverse; long vol di calendario.",
            "analysis": {
                "when_to_use": "Quando si ha una visione neutrale o moderatamente direzionale nel breve termine, ma ci si aspetta un aumento della volatilità implicita nel medio termine. È una scommessa sul tempo e sulla volatilità.",
                "market_conditions": {
                    "optimal": "횡 Mercato laterale nel breve periodo. Volatilità implicita (IV) bassa, specialmente sulla scadenza più lontana, con aspettative di un suo aumento. La curva a termine della volatilità (term structure) è in contango.",
                    "poor": "📈📉 Un forte e rapido movimento direzionale può causare una perdita. Un crollo della volatilità implicita (vega crush) è dannoso."
                },
                "peculiarities": "Il profitto massimo si ottiene se il prezzo del sottostante è esattamente pari allo strike alla data di scadenza della prima opzione (quella venduta). Il **Vega è generalmente positivo**, rendendola una delle poche strategie a trarre profitto da un aumento della IV. Il **Theta è tipicamente positivo** se gestita correttamente."
            }
        },
        "Put Calendar": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Analogo lato put.",
            "analysis": {
                "when_to_use": "Identico al Call Calendar. La scelta può dipendere dallo skew di volatilità (se le put o le call sono relativamente più costose).",
                "market_conditions": { "optimal": "Vedi Call Calendar.", "poor": "Vedi Call Calendar." },
                "peculiarities": "Profilo di rischio/rendimento quasi identico alla versione call."
            }
        },
        "Double Calendar (Time Iron Condor)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10, "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10, "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10, "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Calendario su entrambe le ali; profilo IC nel tempo.",
            "analysis": {
                "when_to_use": "Quando ci si aspetta che il mercato rimanga in un range nel breve termine, combinato con una scommessa long volatility. Simile a un Iron Condor, ma il profitto deriva dal differenziale di theta e vega tra le scadenze.",
                "market_conditions": { "optimal": "Mercato stabile all'interno del range, IV bassa e in aumento.", "poor": "Forte movimento direzionale, crollo della IV." },
                "peculiarities": "Strategia complessa che gioca contemporaneamente su range di prezzo, tempo e volatilità. **Vega e Theta positivi**."
            }
        },
        "Calendar Strangle": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10, "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10, "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10, "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "OTM calendar su entrambi i lati.",
            "analysis": {
                "when_to_use": "Vedi Double Calendar. È un nome alternativo per la stessa strategia.",
                "market_conditions": { "optimal": "Vedi Double Calendar.", "poor": "Vedi Double Calendar." },
                "peculiarities": "Vedi Double Calendar."
            }
        },
        "Calendar Butterfly (Time Fly)": {
            "legs": [],
            "description": "Più calendari concentrati sul centro per picco di vega.",
            "note": "Implementa come somma di calendari con strike centrali."
        },
        "Diagonal Call (Debit)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5, "expiry": "far", "expiry_offset": 30},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5, "expiry": "near", "expiry_offset": 0}
            ],
            "description": "Strike diversi + scadenze diverse.",
            "analysis": {
                "when_to_use": "Simile a un Bull Call Spread, ma con una componente temporale. Si scommette su un rialzo moderato, beneficiando anche del decadimento temporale più rapido dell'opzione venduta.",
                "market_conditions": { "optimal": "Mercato moderatamente rialzista.", "poor": "Mercato ribassista o troppo rialzista." },
                "peculiarities": "Il profilo P/L è simile a un Bull Call Spread ma è 'curvo' a causa del valore temporale residuo della gamba lunga. Il PMCC è una forma di spread diagonale."
            }
        },
        "Diagonal Put (Debit)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 5, "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": 0}
            ],
            "description": "Analogo lato put.",
             "analysis": {
                "when_to_use": "Simile a un Bear Put Spread, ma con una componente temporale. Scommessa moderatamente ribassista.",
                "market_conditions": { "optimal": "Mercato moderatamente ribassista.", "poor": "Mercato rialzista o troppo ribassista." },
                "peculiarities": "Speculare alla versione call."
            }
        },
        "Diagonal Call (Credit)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 5, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Versione credit."
        },
        "Diagonal Put (Credit)": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": 5, "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -5, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Versione credit lato put."
        },
        "Double Diagonal": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5, "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15, "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Diagonale call + diagonale put; profilo IC nel tempo."
        },
        "Diagonal Condor": {
            "legs": [],
            "description": "Quattro gambe diagonali per sagomare P/L temporale.",
            "note": "Somma di due diagonali per lato call/put con strike/tenor differenziati."
        },
    },

    "9. Lizard, Seagull, Reversal & Affini": {
        "Jade Lizard": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15}
            ],
            "description": "Short Put + Call Spread. Obiettivo: zero rischio a rialzo se credito ≥ larghezza call-spread.",
            "analysis": {
                "when_to_use": "Quando si ha una visione neutrale-rialzista e si vuole incassare un premio, ma eliminando completamente il rischio sul lato rialzista.",
                "market_conditions": { "optimal": "Mercato laterale o rialzista. IV alta e in calo.", "poor": "📉 Mercato fortemente ribassista (la short put è a rischio)." },
                "peculiarities": "È una combinazione di una Short Put e un Bear Call Spread. La 'magia' sta nel dimensionare gli strike in modo che il credito totale incassato sia uguale o superiore all'ampiezza del call spread, rendendo impossibile perdere sul lato rialzista."
            }
        },
        "Reverse Jade Lizard": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15}
            ],
            "description": "Speculare, rischio lato ribasso mitigato dalla put long.",
             "analysis": {
                "when_to_use": "Quando si ha una visione neutrale-ribassista e si vuole eliminare il rischio sul lato ribassista.",
                "market_conditions": { "optimal": "Mercato laterale o ribassista. IV alta e in calo.", "poor": "📈 Mercato fortemente rialzista (la short call è a rischio illimitato)." },
                "peculiarities": "Speculare al Jade Lizard. È una combinazione di una Short Call e un Bull Put Spread."
            }
        },
        "Big Lizard": {
            "legs": [
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 25}
            ],
            "description": "Jade con call-spread più largo o credito più alto.",
            "analysis": {
                "when_to_use": "Una variante più aggressiva del Jade Lizard, usata per incassare un credito ancora maggiore, accettando un range più ampio sul lato delle call.",
                "market_conditions": { "optimal": "Vedi Jade Lizard.", "poor": "Vedi Jade Lizard." },
                "peculiarities": "Il termine è informale ('di bottega'). Si riferisce semplicemente a un Jade Lizard con parametri più ampi."
            }
        },
        "Seagull (Bull Capped)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15}
            ],
            "description": "Risk Reversal + opzione aggiuntiva per cap del lato aperto (bull).",
            "analysis": {
                "when_to_use": "Per creare un'esposizione rialzista a costo zero o molto basso, ma con profitti e perdite limitati. È un modo per 'recintare' un trade direzionale.",
                "market_conditions": { "optimal": "Mercato moderatamente rialzista.", "poor": "Mercato fortemente rialzista (il profitto è limitato) o ribassista." },
                "peculiarities": "È una strategia a 3 gambe che può essere vista come un Risk Reversal con un'ala di protezione aggiuntiva, o come un Bull Call Spread finanziato dalla vendita di una put."
            }
        },
    },

    "10. Ladder / Scala / Alberi": {
        "Call Ladder (1:-1:-1)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 20}
            ],
            "description": "Acquisto 1 e vendita multipla su strike superiori.",
            "analysis": {
                "when_to_use": "Quando si è moderatamente rialzisti, ma si vuole anche beneficiare di un mercato laterale, e si crede che un rialzo eccessivo sia improbabile.",
                "market_conditions": { "optimal": "Mercato che sale fino al secondo strike venduto. IV alta e in calo.", "poor": "Mercato che esplode al rialzo oltre l'ultimo strike (rischio illimitato)." },
                "peculiarities": "Simile a un Bull Call Spread, ma con una call extra venduta. Questo aumenta il credito (o riduce il debito) ma introduce un rischio illimitato al rialzo."
            }
        },
        "Put Ladder (1:-1:-1)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -20}
            ],
            "description": "Analogo lato put.",
             "analysis": {
                "when_to_use": "Quando si è moderatamente ribassisti, ma si vuole anche beneficiare di un mercato laterale.",
                "market_conditions": { "optimal": "Mercato che scende fino al secondo strike venduto.", "poor": "Mercato che crolla (rischio significativo)." },
                "peculiarities": "Speculare alla Call Ladder, con rischio significativo al ribasso."
            }
        },
        "Christmas Tree (Call 1x3x2)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -10},
                {"type": "call", "direction": "short", "ratio": 3, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": 15}
            ],
            "description": "Struttura a scalini con quantità 1x3x2."
        },
        "Christmas Tree (Put 1x3x2)": {
            "legs": [
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 10},
                {"type": "put", "direction": "short", "ratio": 3, "moneyness": "ATM"},
                {"type": "put", "direction": "long", "ratio": 2, "strike_offset": -15}
            ],
            "description": "Versione put."
        },
        "Backspread Ladder": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 2, "strike_offset": 10},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 20}
            ],
            "description": "Combinazione di backspread su più livelli per code."
        },
    },

    "11. Arbitraggio, Parità & Carry": {
        "Box Spread (Call+Put Box)": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": -5},
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": 5}
            ],
            "description": "Verticale call + verticale put che replica un bond (carry/arb).",
            "analysis": {
                "when_to_use": "Per strategie di arbitraggio puro sul tasso di interesse. Si crea un prestito o un deposito sintetico, bloccando un profitto privo di rischio (in teoria).",
                "market_conditions": { "optimal": "Quando c'è un mispricing tra le opzioni che permette di bloccare un tasso di interesse superiore a quello risk-free.", "poor": "Mercati efficienti dove tale arbitraggio non è possibile." },
                "peculiarities": "Il grafico P/L è una linea perfettamente piatta. Il profitto o la perdita sono determinati unicamente dal prezzo di esecuzione e non dipendono dal movimento del sottostante. **Tutte le greche sono zero**."
            }
        },
        "Conversion": {
            "legs": [
                {"type": "stock", "direction": "long", "ratio": 1},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Lock-in del carry tramite parità put-call.",
            "analysis": {
                "when_to_use": "Simile al Box Spread, per arbitraggio. Si usa quando la combinazione di opzioni e azioni è prezzata in modo errato rispetto al tasso di interesse.",
                "market_conditions": { "optimal": "Mispricing del mercato.", "poor": "Mercati efficienti." },
                "peculiarities": "Un'altra strategia delta-neutral con P/L piatto. Sfrutta direttamente la formula della parità put-call."
            }
        },
        "Reverse Conversion (Reversal)": {
            "legs": [
                {"type": "stock", "direction": "short", "ratio": 1},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM"},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM"}
            ],
            "description": "Carry inverso (short carry).",
            "analysis": {
                "when_to_use": "L'inverso della Conversion, per sfruttare un mispricing nella direzione opposta.",
                "market_conditions": { "optimal": "Vedi Conversion.", "poor": "Vedi Conversion." },
                "peculiarities": "Profilo di rischio/rendimento identico alla Conversion (piatto)."
            }
        },
        "Jelly Roll": {
            "legs": [
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": 30},
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0}
            ],
            "description": "Call calendar + Put calendar (stesso strike) per rollare il forward/carry."
        },
    },

    "12. Strutture Evento & Vol-Skew": {
        "Iron Fly (Short/Long)": {
            "legs": [],
            "description": "Vedi sezione 6; spesso utilizzata per earnings/eventi.",
            "note": "Short = credit (short vol); Long = debit (long vol)."
        },
        "Calendar su Straddle (ATM)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "short", "ratio": 1, "moneyness": "ATM", "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "moneyness": "ATM", "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Time-spread centrato su ATM per giocare il vega timing."
        },
        "Calendar su Strangle (OTM)": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 10, "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 10, "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -10, "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -10, "expiry": "far", "expiry_offset": 30}
            ],
            "description": "Time-spread OTM su entrambe le ali."
        },
        "Diagonal Strangle": {
            "legs": [
                {"type": "call", "direction": "short", "ratio": 1, "strike_offset": 5, "expiry": "near", "expiry_offset": 0},
                {"type": "call", "direction": "long", "ratio": 1, "strike_offset": 15, "expiry": "far", "expiry_offset": 30},
                {"type": "put", "direction": "short", "ratio": 1, "strike_offset": -5, "expiry": "near", "expiry_offset": 0},
                {"type": "put", "direction": "long", "ratio": 1, "strike_offset": -15, "expiry": "far", "expiry_offset": 30}
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
