from card_holder import Card
from session_holder import Session
import json
import sys
import os
from PyQt6.QtWidgets import QApplication, QDialog
from start import Ui_MainWindow


class Main:
    def __init__(self):
        self.file_name = ""
        self.all_cards = {}
        self.ui = None
        self.app = None
        self.window = None

    def restore(self) -> dict:
        """
        restores program state
        from json file and makes
        dict of cards
        """
        with open(self.file_name, "r") as card_file_restore:
            card_data = json.load(card_file_restore)
            for i in card_data:
                self.all_cards[i] = Card(i, card_data[i]["front"], card_data[i]["back"], card_data[i]["history"])
            return self.all_cards

    def save(self) -> None:
        """
        saves program state
        to json file
        """
        with open(self.file_name, "w") as card_file:  # owerwrights an existing file
            card_data = {}
            for i in self.all_cards:
                card_data[i] = {}
                card_data[i]["front"] = self.all_cards[i].front
                card_data[i]["back"] = self.all_cards[i].back
                card_data[i]["history"] = self.all_cards[i].history
            json.dump(card_data, card_file)
            print(card_data)

    def make_cards(self):
        file = self.ui.lineEdit.text()
        if os.path.isfile(file):
            self.file_name = file
            return self.restore()

    def study(self, mode):
        print(10)
        self.all_cards = self.make_cards()
        if len(self.all_cards) != 0:
            print(20)
            routine = Session(self.window, self.app, self.all_cards, mode)
            routine.process()

    def study_all(self):
        self.study("all")

    def study_essential(self):
        self.study("essential")

    def study_repeat_essential(self):
        self.study("repeat_essential")

    def study_new_ten(self):
        self.study("new_ten")

    def work(self):
        try:
            self.app = QApplication(sys.argv)
            self.window = QDialog()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self.window)
            self.window.show()
            self.ui.pushButton.clicked.connect(state.study_essential)
            self.ui.pushButton_2.clicked.connect(state.study_repeat_essential)
            self.ui.pushButton_3.clicked.connect(state.study_new_ten)
            self.ui.pushButton_4.clicked.connect(state.study_all)
            sys.exit(self.app.exec())
        except SystemExit:
            state.save()


state = Main()
state.work()
