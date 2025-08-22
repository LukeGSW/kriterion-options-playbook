# Contiene le funzioni pure per modificare una struttura di strategia.

def roll_strategy(legs, roll_amount):
    """
    Modifica gli strike di tutte le gambe opzionarie in una strategia.
    Ignora le gambe di tipo 'stock'.
    
    Args:
        legs (list): La lista di dizionari delle gambe della strategia.
        roll_amount (float): Di quanto spostare gli strike (positivo o negativo).
        
    Returns:
        list: La nuova lista di gambe con gli strike aggiornati.
    """
    new_legs = []
    
    for leg in legs:
        new_leg = leg.copy()
        
        # Applica il roll solo alle opzioni, ignora lo stock
        if new_leg.get('type') != 'stock':
            # Il 'moneyness' non è più valido dopo un roll manuale, lo rimuoviamo se esiste
            if 'moneyness' in new_leg:
                del new_leg['moneyness']
            
            # Applica il roll allo strike_offset esistente
            current_offset = new_leg.get('strike_offset', 0)
            new_leg['strike_offset'] = current_offset + roll_amount

        new_legs.append(new_leg)
        
    return new_legs

# Potremo aggiungere qui altre funzioni di aggiustamento, es:
# def add_protection_wing(legs, ...):
#     ...
