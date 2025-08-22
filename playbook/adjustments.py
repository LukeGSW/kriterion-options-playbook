# Contiene le funzioni pure per modificare una struttura di strategia.

def roll_vertical_spread(legs, roll_amount):
    """
    Modifica gli strike di uno spread verticale.
    
    Args:
        legs (list): La lista di dizionari delle gambe della strategia.
        roll_amount (float): Di quanto spostare gli strike (positivo o negativo).
        
    Returns:
        list: La nuova lista di gambe con gli strike aggiornati.
    """
    new_legs = []
    # Assumiamo che uno spread verticale abbia 2 gambe dello stesso tipo
    if len(legs) != 2 or legs[0]['type'] != legs[1]['type']:
        return None # Non è uno spread verticale semplice

    for leg in legs:
        new_leg = leg.copy()
        # Il 'moneyness' non è più valido dopo un roll manuale, usiamo solo l'offset
        if 'moneyness' in new_leg:
            del new_leg['moneyness']
        
        # Applica il roll allo strike_offset esistente
        current_offset = new_leg.get('strike_offset', 0)
        new_leg['strike_offset'] = current_offset + roll_amount
        new_legs.append(new_leg)
        
    return new_legs
