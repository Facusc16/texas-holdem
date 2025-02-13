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


def sort_hand(hole_cards, community_cards, priority=None):
    """Devuelve la mano ordenada"""

    def highest(hand, priority):
        sorted_hand = []

        for card in hand:
            index = deck.index(card)
            sorted_hand.append((card, index))
        sorted_hand.sort(key=lambda x: x[1])

        if "straight" in priority:
            i = 0
            loop = 0
            while i != 6 and loop <= 3:
                if sorted_hand[i][0][1:2] == sorted_hand[i + 1][0][1:2]:
                    sorted_hand.append(sorted_hand[i + 1])
                    sorted_hand.pop(i + 1)
                    loop += 1
                else:
                    i += 1

        return sorted_hand

    def suit(hand):  # pylint: disable=redefined-outer-name
        sorted_hand = [[], [], [], []]

        for card in hand:
            if "♥" in card:
                sorted_hand[0].append(card)
            elif "♦" in card:
                sorted_hand[1].append(card)
            elif "♠" in card:
                sorted_hand[2].append(card)
            elif "♣" in card:
                sorted_hand[3].append(card)

        for suit in sorted_hand:  # pylint: disable=redefined-outer-name
            for i, card in enumerate(suit):
                index = deck.index(card)
                suit[i] = (card, index)
            suit.sort(key=lambda x: x[1])

        sorted_hand.sort(key=len, reverse=True)

        sorted_hand = sum(sorted_hand, [])

        return sorted_hand

    def value(hand):  # pylint: disable=redefined-outer-name
        sorted_hand = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        for card in hand:
            if "A" in card:
                sorted_hand[0].append(card)
            elif "K" in card:
                sorted_hand[1].append(card)
            elif "Q" in card:
                sorted_hand[2].append(card)
            elif "J" in card:
                sorted_hand[3].append(card)
            elif "10" in card:
                sorted_hand[4].append(card)
            elif "9" in card:
                sorted_hand[5].append(card)
            elif "8" in card:
                sorted_hand[6].append(card)
            elif "7" in card:
                sorted_hand[7].append(card)
            elif "6" in card:
                sorted_hand[8].append(card)
            elif "5" in card:
                sorted_hand[9].append(card)
            elif "4" in card:
                sorted_hand[10].append(card)
            elif "3" in card:
                sorted_hand[11].append(card)
            elif "2" in card:
                sorted_hand[12].append(card)

        sorted_hand.sort(key=len, reverse=True)

        sorted_hand = sum(sorted_hand, [])

        return sorted_hand

    hand = hole_cards + community_cards
    sorted_hand = []

    if "highest" in priority:
        sorted_hand = highest(hand, priority)

    elif priority == "suit":
        sorted_hand = suit(hand)

    elif priority == "value":
        sorted_hand = value(hand)

    return sorted_hand


def calculate_combination(hand):
    """Devuelve la combinación más alta formada"""

    combination = None

    if [x[0] for x in hand[:5]] in [
            list(f"[{value}{suit}]" for value in ["A", "K", "Q", "J", "10"]) for suit in "♥♦♠♣"]:
        combination = "ESCALERA REAL"

    print(combination)


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

    # Asigno cartas al jugador, a la máquina y a la mesa
    # user_cards, machine_cards, table_cards = define_cards() # cambiar nombre de user_cards

    player_cards = ['[3♠]', '[10♣]']
    community_cards = ['[3♦]', '[3♣]', '[10♠]', '[8♠]', '[7♣]']

    # machine_cards = ["[2♣]", "[9♠]"]

    # Ordeno la mano del jugador
    player_hand = sort_hand(player_cards, community_cards,
                            priority="value")
    print(player_hand)

    # calculate_combination(player_hand)

    # game(user_cards, machine_cards, table_cards)


if __name__ == "__main__":
    main()
