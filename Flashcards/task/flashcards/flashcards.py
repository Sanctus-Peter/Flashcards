import json
import sys
from io import StringIO


class FlashCard:
    __ops = [
        "add", "remove", "import",
        "export", "ask", "reset stats",
        "log", "hardest card", "exit"
    ]

    def __init__(self):
        self.__flash_card = {}
        self.log_file = StringIO()
        self.extern_save = 0
        self.extern_file_name = None

    def get_key(self, value):
        return next((k for k, v in self.__flash_card.items() if v == value), None)

    def value_in_dict(self, d, value):
        for k, v in d.items():
            if v == value:
                return True
            elif isinstance(v, dict):
                if self.value_in_dict(v, value):
                    return True
        return False

    def add_card(self):
        card = input("The card:\n")
        self.log_file.write("The card:\n")
        while card in self.__flash_card.keys():
            print(f"The term \"{card}\" already exists. Try again:")
            self.log_file.write(f"The term \"{card}\" already exists. Try again:\n")
            card = input()

        definition = input("The definition for card:\n")
        self.log_file.write("The definition for card:\n")
        for term, _def in self.__flash_card.items():
            while definition == _def["definition"]:
                print(f"The definition \"{definition}\" already exists. Try again:")
                self.log_file.write(f"The definition \"{definition}\" already exists. Try again:\n")
                definition = input()

        while self.value_in_dict(self.__flash_card, definition):
            print(f"The definition \"{definition}\" already exists. Try again:")
            self.log_file.write(f"The definition \"{definition}\" already exists. Try again:\n")
            definition = input()

        self.__flash_card[card] = {"definition": definition, "mistakes": 0}
        print(f"The pair (\"{card}\": \"{definition}\") has been added.")
        self.log_file.write(f"The pair (\"{card}\": \"{definition}\") has been added.\n")

    def remove_card(self):
        card_to_remove = input("Which card?\n")
        self.log_file.write("Which card?\n")
        if card_to_remove not in self.__flash_card.keys():
            print(f"Can't remove \"{card_to_remove}\": there is no such card.")
            self.log_file.write(f"Can't remove \"{card_to_remove}\": there is no such card.\n")
        else:
            del self.__flash_card[card_to_remove]
            print("The card has been removed.")
            self.log_file.write("The card has been removed.\n")

    def import_card(self, var=None):
        if var:
            file_name = var
        else:
            file_name = input("File name:\n")
            self.log_file.write("File name:\n")
        try:
            with open(file_name, 'r') as f:
                imported_cards = json.loads(f.read())
        except FileNotFoundError:
            print("File not found")
            self.log_file.write("File not found\n")
            return

        for k, v in imported_cards.items():
            if k in self.__flash_card.keys():
                self.__flash_card[k] = v
            self.__flash_card[k] = v
        print(f"{len(imported_cards)} cards have been loaded.")
        self.log_file.write(f"{len(imported_cards)} cards have been loaded.\n")

    def export_card(self, var=None):
        if var:
            file_name = var
        else:
            file_name = input("File name:\n")
            self.log_file.write("File name:\n")

        with open(file_name, 'a') as f:
            f.write(json.dumps(self.__flash_card))

        print(f"{len(self.__flash_card)} cards have been saved.")
        self.log_file.write(f"{len(self.__flash_card)} cards have been saved.\n")

    def log_card(self):
        log_file = input("File name:\n")
        self.log_file.write("File name:\n")
        try:
            with open(log_file, 'w') as log:
                for line in self.log_file.getvalue():
                    log.write(line)
                print("The log has been saved.")
        except NotImplementedError:
            self.log_file.write(f"Error saving log to file {log_file}")
        except FileNotFoundError:
            self.log_file.write(f"Failed, {log_file} not found")

    def hardest_card(self):
        max_mistakes = 0
        hardest_cards = []
        for k, v in self.__flash_card.items():
            if v["mistakes"] > max_mistakes:
                max_mistakes = v["mistakes"]
                hardest_cards = [k]
            elif v["mistakes"] == max_mistakes:
                hardest_cards.append(k)
        if max_mistakes == 0:
            print("There are no cards with errors.")
            self.log_file.write("There are no cards with errors.\n")
        elif len(hardest_cards) == 1:
            print(f"The hardest card is \"{hardest_cards[0]}\". You have {max_mistakes} errors answering it.")
            self.log_file.write(
                f"The hardest card is \"{hardest_cards[0]}\". You have {max_mistakes} errors answering it.\n"
            )
        else:
            print(f"The hardest cards are {', '.join(hardest_cards)}. You have {max_mistakes} errors answering them.")
            self.log_file.write(
                f"The hardest cards are {', '.join(hardest_cards)}. You have {max_mistakes} errors answering them.\n"
            )

    def reset_stats(self):
        for k, v in self.__flash_card.items():
            v["mistakes"] = 0
        print("Card statistics have been reset.")
        self.log_file.write("Card statistics have been reset.\n")

    def ask(self):
        n_card = int(input("How many times to ask?\n"))
        self.log_file.write("How many times to ask?\n")
        count = 1
        n_read = (n_card // len(self.__flash_card)) + 1\
            if n_card != len(self.__flash_card) else (n_card // len(self.__flash_card))
        for _ in range(n_read):
            for key, value in self.__flash_card.items():
                answer = input(f"Print the definition of \"{key}\":\n")
                self.log_file.write(f"Print the definition of \"{key}\":\n")
                if answer != value:
                    self.__flash_card[key]["mistakes"] += 1
                    if self.value_in_dict(self.__flash_card, answer):
                        print(
                            f"Wrong. The right answer is \"{value}\",",
                            f"but your definition is correct for \"{self.get_key(answer)}\"."
                        )
                        self.log_file.write(
                            f"Wrong. The right answer is \"{value}\"," +
                            f"but your definition is correct for \"{self.get_key(answer)}\".\n"
                        )
                    else:
                        print(f"Wrong. The right answer is \"{value}")
                        self.log_file.write(f"Wrong. The right answer is \"{value}\n")
                else:
                    print("correct!")
                    self.log_file.write("correct!\n")
                if count == n_card:
                    break
                count += 1

    @staticmethod
    def exit():
        print("Bye bye!")
        sys.exit(0)

    def main(self):
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                if arg.startswith("--import"):
                    self.extern_file_name = arg.split("=")[1]
                    self.import_card(self.extern_file_name)
                elif arg.startswith("--export"):
                    self.extern_file_name = arg.split("=")[1]
                    self.extern_save = 1

        op = input(
            "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n"
        )
        self.log_file.write(
            f"Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n"
        )
        if op not in self.__ops:
            return
        if op == "add":
            self.add_card()
        elif op == "remove":
            self.remove_card()
        elif op == "import":
            self.import_card()
        elif op == "export":
            self.export_card()
        elif op == "ask":
            self.ask()
        elif op == "log":
            self.log_card()
        elif op == "hardest card":
            self.hardest_card()
        elif op == "reset stats":
            self.reset_stats()
        elif op == "exit":
            if self.extern_save:
                self.export_card(self.extern_file_name)
            self.exit()
        else:
            print("Invalid operation")

    def loop(self):
        while True:
            self.main()


if __name__ == '__main__':
    FlashCard().loop()
