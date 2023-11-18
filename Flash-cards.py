import json

from card_holder import Card
from session_holder import Session

def restore() -> dict:
    """
    restores programm state
    from json file and makes
    dict of cards
    """""
    global file_name
    with open(file_name, "r") as card_file_restore:
        card_data = json.load(card_file_restore)
        all_cards = {}
        for i in card_data:
            all_cards[i] = Card(i, card_data[i]["front"], card_data[i]["back"], card_data[i]["history"])
        return all_cards


def save() -> None:
    """
    Saves program
    state to json file
    """
    global file_name
    global all_cards
    with open(file_name, "w") as card_file:  # owerwrights an existing file
        card_data = {}
        for i in all_cards:
            card_data[i] = {}
            card_data[i]["front"] = all_cards[i].front
            card_data[i]["back"] = all_cards[i].back
            card_data[i]["history"] = all_cards[i].history
        json.dump(card_data, card_file)
        print(card_data)


file_name = "MyCards.json"
try:
    all_cards = restore()
    routine = Session(all_cards, "essential")
    routine.process()
    save()
except KeyboardInterrupt:
    save()
