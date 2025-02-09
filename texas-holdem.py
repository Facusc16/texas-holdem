import random
from os import system

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


def show_cards(user_cards, table_cards, round_number, turn):
    print("♥ ♣ TEXAS HOLDEM ♦ ♠\n")

    print(f"{turn}\n")

    print("Cartas de la máquina:      [¿?][¿?]\n")

    if round_number == 0:
        print(
            f"Cartas en mesa:      {table_cards[0]}{table_cards[1]}[¿?][¿?][¿?]\n")
    elif round_number == 1:
        print(
            f"Cartas en mesa:      {table_cards[0]}{table_cards[1]}{table_cards[2]}[¿?][¿?]\n")
    elif round_number == 2:
        print(
            f"Cartas en mesa:      {table_cards[0]}{table_cards[1]}{table_cards[2]}{table_cards[3]}[¿?]\n")
    elif round_number == 3:
        print(
            f"Cartas en mesa:      {table_cards[0]}{table_cards[1]}{table_cards[2]}{table_cards[3]}{table_cards[4]}\n")

    print(f"Tus cartas:                {user_cards[0]}{user_cards[1]}")


def machine_play(user_cards, table_cards, round_number):

    show_cards(user_cards, table_cards, round_number, "Máquina")
    input("\nENTER para continuar...")
    system("cls")

    bet = False
    if random.randint(1, 2) in (1, 2):  # Implementación temporal para testeo.
        bet = True

    return bet


def player_play(user_cards, table_cards, round_number):

    show_cards(user_cards, table_cards, round_number, "Jugador")

    bet = None
    if input("\n¿Desea seguir jugando? [Y/N]: ").lower() == "y":
        bet = True
    else:
        bet = False
    system("cls")

    return bet


def game(user_cards, table_cards):
    system("cls")
    round_number = 0

    while not round_number == 3:

        machine_bet = machine_play(user_cards, table_cards, round_number)
        if not machine_bet:
            break

        player_bet = player_play(user_cards, table_cards, round_number)
        if not player_bet:
            break

        round_number += 1


def main():
    user_cards, machine_cards, table_cards = define_cards()

    game(user_cards, table_cards)


if __name__ == "__main__":
    main()
