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
        global all_cards
        for i in card_data:
            all_cards[i] = Card(i, card_data[i]["front"], card_data[i]["back"], card_data[i]["history"])
        return all_cards


def save(file_name, all_cards) -> None:
    """
    Saves program
    state to json file
    """
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
    global file_name
    file = ui.lineEdit.text()
    if os.path.isfile(file):
        file_name = file
        return restore(file)




def study(mode):
    print(10)
    global all_cards
    all_cards = make_cards()
    if len(all_cards) != 0:
        print(20)
        global app
        global window
        routine = Session(window, app, all_cards, mode)
        routine.process()

def study_all():
    study("all")


def study_essential():
    study("essential")


def study_repeat_essential():
    study("repeat_essential")


def study_new_ten():
    study("new_ten")


file_name = ""
all_cards = {}
try:
    app = QApplication(sys.argv)
    window = QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    ui.pushButton.clicked.connect(study_essential)
    ui.pushButton_2.clicked.connect(study_repeat_essential)
    ui.pushButton_3.clicked.connect(study_new_ten)
    ui.pushButton_4.clicked.connect(study_all)
    sys.exit(app.exec())
except SystemExit:
    save(file_name, all_cards)
