import random
import json
import time


class Card:
    def __init__(self, name, front, back, history: dict, flipped=0) -> None:
        self.name = name
        self.front = front
        self.back = back
        if history is None:
            history = []
        self.history = history
        self.flipped = flipped
        self.passed_number = len([i for i in history if i["result"] == "passed"])
        if self.passed_number == 0:
            self.last_passed_time = -1  # -1 if card was never studied
        else:
            self.last_passed_time = [i for i in history if i["result"] == "passed"][-1]["time"]

    def flip(self) -> None:
        self.flipped = 1 - self.flipped

    def show(self) -> None:
        shown = (self.front, self.back)[self.flipped]
        print(shown)

    def update_history(self, result: str) -> None:
        self.history.append({"time": int(time.time()), "result": result})

    def ask(self) -> str:
        self.show()
        input("Напишите что-то, чтобы увидеть ответ")
        self.flip()
        self.show()
        self.flip()
        from_user = input('"passed" - правильный ответ, "failed" - неправильный ответ, другой - не учитывать ответ\n')
        if from_user == "passed":
            print("Ответ верный")
            self.update_history("passed")
        elif from_user == "failed":
            print("Ответ неверный")
            self.update_history("failed")
        else:
            print("Ответ не будет учтен")
        return from_user


class Session:
    def __init__(self, all_cards: dict, mode="all") -> None:
        self.mode = mode
        self.all_cards = all_cards
        self.session_cards = {}

    def choose_cards(self):
        """"
        modes:
        all -> you will see all cards until you answer all of them right\n
        essential -> you will see only cards that you haven't reminded for
        a long period of time or haven't seen at all\n
        repeat_essential -> you will see only cards that you have already seen but a long time ago\n
        new_10 -> you will see 10 cards you have not seen yet (or less if it is not possible)
        """
        if self.mode == "all":
            self.session_cards = self.all_cards.copy()
        if self.mode == "essential":
            working_cards = {}
            for i in all_cards.copy().values():
                if i.last_passed_time <= time.time() - 4**i.passed_number * 800:
                    working_cards[i.name] = i
            self.session_cards = working_cards
        if self.mode == "repeat_essential":
            working_cards = {}
            for i in all_cards.copy().values():
                working_cards = {}
                if i.last_passed_time <= time.time() - 4**i.passed_number * 800 and len(i.history) > 0:
                    working_cards[i.name] = i
            self.session_cards = working_cards
        if self.mode == "new_10":
            working_cards = {}
            for i in all_cards.copy().values():
                if len(i.history) == 0:
                    working_cards[i.name] = i
                if len(working_cards) >= 10:
                    break
            self.session_cards = working_cards

    def pull_out(self) -> str:
        key = random.choice(list(self.session_cards.keys()))
        return key
        
    def process(self) -> None:
        self.choose_cards()
        while len(self.session_cards) != 0:
            key = self.pull_out()
            current_card = self.all_cards[key]
            result = current_card.ask()
            if result == "passed":
                self.session_cards.pop(key)


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
