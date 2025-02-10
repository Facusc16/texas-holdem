"""Módulo para simular partida de Texas Holdem"""

import random
from os import system

# Crear lista de maso de cartas
deck = []
for value in "A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2":
    for suit in "♥♦♠♣":
        deck.append(f"[{value}{suit}]")


def define_cards():
    """Asigna cartas al jugador, a la máquina y a la mesa"""
    shuffled_deck = random.sample(deck, len(deck))

    chosen_cards = []
    user_cards = []
    machine_cards = []
    table_cards = []

    while len(chosen_cards) < 9:
        card = random.choice(shuffled_deck)

        if card not in chosen_cards:
            chosen_cards.append(card)

            if len(user_cards) < 2:
                user_cards.append(card)

            elif len(machine_cards) < 2:
                machine_cards.append(card)

            else:
                table_cards.append(card)

    return user_cards, machine_cards, table_cards


def show_cards(user_cards, table_cards, turn, round_number=None, machine_cards=None):
    """Muestras las cartas, según las situación unas u otras"""

    print("♥ ♣ TEXAS HOLDEM ♦ ♠\n")

    print(f"{turn}\n")

    # Imprime las cartas de la máquina
    if turn != "Fin de la mano":
        print("Cartas de la máquina:      [¿?][¿?]\n")
    else:
        print(
            f"Cartas de la máquina:      {"".join(machine_cards)}\n")

    # Imprime las cartas de la mesa
    if round_number == 0 and turn != "Fin de la mano":
        print(f"Cartas en mesa:      {"".join(table_cards[:3])}[¿?][¿?]\n")

    elif round_number == 1 and turn != "Fin de la mano":
        print(f"Cartas en mesa:      {"".join(table_cards[:4])}[¿?]\n")

    elif round_number in (2, 3) or turn == "Fin de la mano":
        print(f"Cartas en mesa:      {"".join(table_cards)}\n")

    # Imprime las cartas del jugador
    print(f"Tus cartas:                {"".join(user_cards)}")


def machine_play(user_cards, table_cards, round_number):
    """Controla el turno de la máquina"""

    show_cards(user_cards, table_cards, "Máquina", round_number)
    input("\nENTER para continuar...")
    system("cls")

    bet = False
    if random.randint(1, 2) in (1, 2):  # Implementación temporal para testeo.
        bet = True

    return bet


def player_play(user_cards, table_cards, round_number):
    """Controla el turno del jugador"""

    show_cards(user_cards, table_cards, "Jugador", round_number)

    if input("\n¿Desea seguir jugando? [Y/N]: ").lower() == "y":
        bet = True
    else:
        bet = False
    system("cls")

    return bet


def game(user_cards, machine_cards, table_cards):
    """Ejecuta el juego"""

    system("cls")
    round_number = 0

    while round_number != 3:

        machine_bet = machine_play(
            user_cards, table_cards, round_number)
        if not machine_bet:
            break

        player_bet = player_play(
            user_cards, table_cards, round_number)
        if not player_bet:
            break

        round_number += 1

    if not machine_bet:
        show_cards(user_cards, table_cards, "Fin de la mano", round_number=round_number,
                   machine_cards=machine_cards)
        print("\nLa máquina se ha retirado. ¡Ganaste la mano!")
    elif not player_bet:
        show_cards(user_cards, table_cards, "Fin de la mano", round_number=round_number,
                   machine_cards=machine_cards)
        print("\nTe has retidado, perdiste la mano")
    elif round_number == 3:
        show_cards(user_cards, table_cards, "Fin de la mano", round_number=round_number,
                   machine_cards=machine_cards)
        print("\nPROXIMAMENTE...")  # Definir forma de calcular el ganador


def main():
    """Ejecuta el programa entero"""

    user_cards, machine_cards, table_cards = define_cards()

    game(user_cards, machine_cards, table_cards)


if __name__ == "__main__":
    main()
