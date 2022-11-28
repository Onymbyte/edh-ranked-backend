import urllib.request as req
import urllib.error
import json
from models import Listing, Cards
from app import db
from time import sleep



def addCommander(name):
    try:
        card = json.loads(req.urlopen(f"https://api.scryfall.com/cards/named?fuzzy={name.replace(' ', '+')}").read())
    except urllib.error.HTTPError:
        print("Card did not exist.")
        return False
    with open('response.json', 'w') as f:
        json.dump(card, f)
    if Listing.query.filter_by(uuid= card['id']).first() is not None:
        print('Listing already in database.')
        return False
    if (not ('Legendary Creature' in card['type_line'])) and (not ('can be your commander' in card['oracle_text'])):
        print(f"Card was not a Legendary Creature: {card['type_line']} or cannot be your commander")
        return False
    listing = Listing(uuid=card['id'], name=card['name'], mana_cost=card['mana_cost'], color_identity="".join(card['color_identity']), cmc=card['cmc'])
    db.session.add(listing)
    db.session.commit()
    return listing.id

def getImage(id, size="small"):
    card = json.loads(req.urlopen(f"https://api.scryfall.com/cards/{id}").read())
    sleep(0.1)
    return card['image_uris'][size]
def addCard(name, listing):
    try:
        card = json.loads(req.urlopen(f"https://api.scryfall.com/cards/named?fuzzy={name.replace(' ', '+')}").read())
    except urllib.error.HTTPError:
        print("Card did not exist.")
        return False
    with open('response.json', 'w') as f:
        json.dump(card, f)
    if set(card['color_identity']) - set(listing.color_identity):
        print("Card could not be in this deck based on color.")
        return False
    _card = Cards.query.filter_by(uuid= card['id']).first()
    if _card is not None:
        print('Card already in database.')
        return _card.id
    _card = Cards(uuid=card['id'], name=card['name'])
    db.session.add(_card)
    db.session.commit()
    return _card.id

    