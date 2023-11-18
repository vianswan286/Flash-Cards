import time


class Card:
    def __init__(self, name: str, front: str, back: str, history: dict, flipped=0) -> None:
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
        """
        Method asks user current card and changes history dependent on results
        """
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