import sys
import json
from PyQt6.QtWidgets import QApplication, QDialog
from ui_imagedialog import Ui_SubWindow
from card_holder import Card

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


def func():
    global i
    global ui
    i += 1
    ui.textBrowser.setText(str(i))


app = QApplication(sys.argv)
window = QDialog()
ui = Ui_SubWindow()
ui.setupUi(window)
window.show()
# ui.pushButton_2.clicked.connect(self.show_answer)
#  pushButton_3.clicked.connect(self.keep_showing)
sys.exit(app.exec())
