import random

# Crear lista de maso de cartas
maso = ["[A♠]", "[2♠]", "[3♠]", "[4♠]", "[5♠]", "[6♠]", "[7♠]", "[8♠]", "[9♠]", "[10♠]", "[J♠]", "[Q♠]", "[K♠]",
        "[A♣]", "[2♣]", "[3♣]", "[4♣]", "[5♣]", "[6♣]", "[7♣]", "[8♣]", "[9♣]", "[10♣]", "[J♣]", "[Q♣]", "[K♣]",
        "[A♥]", "[2♥]", "[3♥]", "[4♥]", "[5♥]", "[6♥]", "[7♥]", "[8♥]", "[9♥]", "[10♥]", "[J♥]", "[Q♥]", "[K♥]",
        "[A♦]", "[2♦]", "[3♦]", "[4♦]", "[5♦]", "[6♦]", "[7♦]", "[8♦]", "[9♦]", "[10♦]", "[J♦]", "[Q♦]", "[K♦]"]


def define_cards():
    chosen_cards = []
    user_cards = []
    machine_cards = []
    table_cards = []

    while len(chosen_cards) < 9:
        card = random.choice(maso)

        if card not in chosen_cards:
            chosen_cards.append(card)

            if len(user_cards) < 2:
                user_cards.append(card)

            elif len(machine_cards) < 2:
                machine_cards.append(card)

            else:
                table_cards.append(card)

    return user_cards, machine_cards, table_cards


def main():
    user_cards, machine_cards, table_cards = define_cards()


if __name__ == "__main__":
    main()
