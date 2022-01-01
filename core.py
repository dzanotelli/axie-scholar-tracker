from db.models import Scholar


def add_scholar(name, ronin_id, **kwargs):
    # optional fields
    internal_id = kwargs.get('internal_id', None)
    battle_name = kwargs.get('battle_name', None)

    s = Scholar()
    s.name = name
    s.ronin_id = ronin_id
    s.internal_id = internal_id
    s.battle_name = battle_name
    s.save()
    
