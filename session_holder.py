import time
import random
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout
from ui_imagedialog import Ui_SubWindow


class Session:
    def __init__(self,window, app, all_cards: dict, mode="all") -> None:
        self.mode = mode
        self.all_cards = all_cards
        self.session_cards = {}
        self.current_card = None
        self.app = app
        self.window = window
    def choose_cards(self):
        """"
        modes:
        all -> you will see all         #self.ui.add(self.window)
cards until you answer all of them right\n
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

    def pull_out(self):
        key = random.choice(list(self.session_cards.keys()))
        self.current_card = self.session_cards[key]
        self.current_card.flipped = 0

    def remembered(self):
        if len(self.session_cards) == 0:
            self.ui.textBrowser.setText("Cards have finished")
            return
        self.session_cards.pop(self.current_card.name)
        self.current_card.update_history("passed")
        self.all_cards[self.current_card.name].history.append(self.current_card.history[-1])
        if len(self.session_cards) == 0:
            self.ui.textBrowser.setText("Cards have finished")
            return
        self.pull_out()
        self.ui.textBrowser.setText(self.current_card.show())

    def show_answer(self):
        if len(self.session_cards) == 0:
            self.ui.textBrowser.setText("Cards have finished")
            return
        self.current_card.flip()
        self.ui.textBrowser.setText(self.current_card.show())

    def keep_showing(self):
        if len(self.session_cards) == 0:
            self.ui.textBrowser.setText("Cards have finished")
            return
        self.pull_out()
        self.ui.textBrowser.setText(self.current_card.show())

    def process(self) -> None:
        self.choose_cards()
        self.pull_out()
        print(10)
        self.new_window = QDialog(self.window)
        self.ui = Ui_SubWindow()
        self.ui.setupUi(self.new_window)
        self.new_window.show()
        #add this into the event loop
        self.ui.textBrowser.setText(self.current_card.show())
        self.ui.pushButton.clicked.connect(self.remembered)
        self.ui.pushButton_2.clicked.connect(self.show_answer)
        self.ui.pushButton_3.clicked.connect(self.keep_showing)
        self.show_answer()
        #add this into the event loop
