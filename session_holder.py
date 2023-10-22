import time
import random


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
            for i in self.all_cards.copy().values():
                if i.last_passed_time <= time.time() - 4 ** i.passed_number * 800:
                    working_cards[i.name] = i
            self.session_cards = working_cards
        if self.mode == "repeat_essential":
            working_cards = {}
            for i in self.all_cards.copy().values():
                working_cards = {}
                if i.last_passed_time <= time.time() - 4 ** i.passed_number * 800 and len(i.history) > 0:
                    working_cards[i.name] = i
            self.session_cards = working_cards
        if self.mode == "new_10":
            working_cards = {}
            for i in self.all_cards.copy().values():
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

