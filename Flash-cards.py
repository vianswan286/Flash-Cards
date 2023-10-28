from card_holder import Card
from session_holder import Session
import json
import sys
import os
from PyQt6.QtWidgets import QApplication, QDialog
from start import Ui_MainWindow


def restore(file_name) -> dict:
    """
    restores program state
    from json file and makes
    dict of cards
    """
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


def make_cards():
    file = ui.lineEdit.text()
    if os.path.isfile(file):
        return restore(file)


def study_all():
    all_cards = make_cards()
    if all_cards:
        global app
        global window
        routine = Session(window, app, all_cards, "all")
        routine.process()


try:
#    all_cards = restore()
    app = QApplication(sys.argv)
    window = QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    ui.pushButton_4.clicked.connect(study_all)
# ui.pushButton_2.clicked.connect(self.show_answer)
# pushButton_3.clicked.connect(self.keep_showing)
    sys.exit(app.exec())
#   routine = Session(all_cards)
#   routine.process()
except SystemExit:
    save()
