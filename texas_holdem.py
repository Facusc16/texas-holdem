"""Módulo para simular partida de Texas Holdem"""

import random
from os import system
import re

# Crear lista de maso de cartas
value_deck = [[], [], [], [], [], [], [], [], [], [], [], [], []]
for i, value in enumerate(("A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2")):
    for suit in "♥♦♠♣":
        value_deck[i].append(f"[{value}{suit}]")

deck = sum(value_deck, [])


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


def show_cards(user_cards, community_cards, turn, round_number=None, machine_cards=None):
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
        print(f"Cartas en mesa:      {"".join(community_cards[:3])}[¿?][¿?]\n")

    elif round_number == 1 and turn != "Fin de la mano":
        print(f"Cartas en mesa:      {"".join(community_cards[:4])}[¿?]\n")

    elif round_number in (2, 3) or turn == "Fin de la mano":
        print(f"Cartas en mesa:      {"".join(community_cards)}\n")

    # Imprime las cartas del jugador
    print(f"Tus cartas:                {"".join(user_cards)}")


def sort_hand(hand, priority=None):
    """Devuelve la mano ordenada"""

    def highest(hand, priority):
        sorted_hand = hand[:]
        sorted_hand.sort(key=deck.index)

        if "straight" in priority:

            i = 0  # pylint: disable=redefined-outer-name
            loop = 0
            while i != len(sorted_hand) - 1 and loop <= 3:
                if sorted_hand[i][1:2] == sorted_hand[i + 1][1:2]:
                    sorted_hand.append(sorted_hand[i + 1])
                    sorted_hand.pop(i + 1)
                    loop += 1
                else:
                    i += 1

            index_0 = None
            index_1 = None
            index_2 = None
            index_3 = None

            for card in sorted_hand:
                for group in value_deck:
                    if card in group:

                        if index_0 is None:
                            index_0 = value_deck.index(group)
                            break

                        elif index_1 is None:
                            index_1 = value_deck.index(group)
                            break

                        elif index_2 is None:
                            index_2 = value_deck.index(group)
                            break

                        elif index_3 is None:
                            index_3 = value_deck.index(group)
                            break

            if index_0 - index_1 != -1 and index_1 - index_2 == -1 and index_2 - index_3 == -1:
                sorted_hand.insert(-1, sorted_hand[0])
                del sorted_hand[0]

            elif ((index_0 - index_1 == -1 or index_0 - index_1 != -1)
                  and index_1 - index_2 != -1 and index_2 - index_3 == -1):

                sorted_hand.extend([sorted_hand[0], sorted_hand[1]])
                del sorted_hand[0:2]

            elif ((index_0 - index_1 == -1 or index_0 - index_1 != -1)
                  and (index_1 - index_2 == -1 or index_1 - index_2 != -1)
                  and index_2 - index_3 != -1):

                sorted_hand.extend([sorted_hand[0],
                                    sorted_hand[1],
                                    sorted_hand[2]])
                del sorted_hand[0:3]

            if ("2" in sorted_hand[3] and "A" not in sorted_hand[4]
                    and ("A" in sorted_hand[5] or "A" in sorted_hand[6])):

                for i, card in enumerate(sorted_hand):
                    if "A" in card:
                        sorted_hand.insert(-3, sorted_hand[i])
                        sorted_hand.pop(i + 1)
                        break

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
            suit.sort(key=deck.index)

        sorted_hand.sort(key=len, reverse=True)

        sorted_hand = sum(sorted_hand, [])

        return sorted_hand

    def value(hand):  # pylint: disable=redefined-outer-name
        sorted_hand = [[], [], [], [], [], [], []]

        hand.sort(key=deck.index)
        for card in hand:
            for value in sorted_hand:  # pylint: disable=redefined-outer-name
                if len(value) == 0 or card[1:2] in value[0]:
                    value.append(card)
                    break

        sorted_hand.sort(key=len, reverse=True)

        if (len(sorted_hand[0]) > 3 and len(sorted_hand[1]) == 2):
            sorted_hand = [sorted_hand[0]] + [sum(sorted_hand[1:], [])]
            sorted_hand[1].sort(key=deck.index)

        elif len(sorted_hand[0]) == 2 and len(sorted_hand[1]) == 2 and len(sorted_hand[2]) == 2:
            sorted_hand = sorted_hand[:2] + [sum(sorted_hand[2:], [])]
            sorted_hand[2].sort(key=deck.index)

        sorted_hand = sum(sorted_hand, [])

        return sorted_hand

    sorted_hand = []

    if "highest" in priority:
        sorted_hand = highest(hand, priority)

    elif priority == "suit":
        sorted_hand = suit(hand)

    elif priority == "value":
        sorted_hand = value(hand)

    return sorted_hand


# En las que devuelve con slicing, devuelve una lista. Y juntas todo el código de la carta
def analyze_hand(hand):
    """Devuelve las características de la mano"""

    def straight_combination(hand):
        hand = sort_hand(hand, priority="highest.straight")

        numbers = [int(n) if n.isdigit() else n for card in hand[:5]
                   for n in re.findall(r"\[(\d{1,2}|[JQKA])[♥♦♠♣]\]", card)]

        for i, n in enumerate(numbers):  # pylint: disable=redefined-outer-name
            if isinstance(n, str):
                if n == "A":
                    numbers[i] = 14 if i == 0 else 1
                elif n == "K":
                    numbers[i] = 13
                elif n == "Q":
                    numbers[i] = 12
                elif n == "J":
                    numbers[i] = 11

        if [numbers[i] - numbers[i + 1] for i in range(len(numbers) - 1)] == [1, 1, 1, 1]:
            return f"escalera {hand[0][1:2]}"

    def flush_combination(hand, straight=False):
        if straight:
            hand = sort_hand(hand, priority="highest.straight")
        else:
            hand = sort_hand(hand, priority="suit")

        reference = None
        for card in hand[:5]:
            if reference is None:
                reference = card[-2]
            elif reference != card[-2]:
                return False

        return f"color {hand[0][1:2]}{hand[1][1:2]}{hand[2][1:2]}{hand[3][1:2]}{hand[4][1:2]}"

    def value_combination(hand):
        hand = sort_hand(hand, priority="value")

        group_1 = []
        group_2 = []
        group_3 = []

        for card in hand[:5]:
            if len(group_1) == 0:
                group_1.append(card[1:2])

            elif card[1:2] == group_1[0]:
                group_1.append(card[1:2])

            elif len(group_2) == 0:
                group_2.append(card[1:2])

            elif card[1:2] == group_2[0]:
                group_2.append(card[1:2])

            else:
                group_3.append(card[1:2])

        hand_values = [n for card in hand for n in re.findall(
            r"\[(\d{1,2}|[JQKA])", card)]
        hand_values = hand_values[:5]

        if len(group_1) == 4:
            return f"poker {hand_values[-1]}"
        elif len(group_1) == 3 and len(group_2) == 2:
            return f"full{hand_values[0]}{hand_values[3]}"
        elif len(group_1) == 3 and len(group_2) < 2:
            return f"trio{hand_values[0]} {hand_values[3:]}"
        elif len(group_1) == 2 and len(group_2) == 2:
            return f"doble pareja{hand_values[0]}{hand_values[2]} {hand_values[-1]}"
        elif len(group_1) == 2 and len(group_2) < 2:
            return f"pareja{hand_values[0]} {hand_values[2:]}"
        else:
            return False

    if (straight := straight_combination(hand)):

        if (flush := flush_combination(hand, straight=True)):
            # Esto no va a estar ordenado, así que puede ser escalera real y que no lo devuelva como tal
            if straight[-1] == "A":
                return straight[:8] + " real"
            else:
                return straight[:8] + " " + flush[:7]
        else:
            return straight

    elif (flush := flush_combination(hand)):
        return flush

    elif (combination := value_combination(hand)):
        return combination

    else:
        hand_values = [n for card in hand for n in re.findall(
            r"\[(\d{1,2}|[JQKA])", card)]

        return f"carta alta {hand_values[:5]}"


def machine_play(machine_cards, community_cards, player_cards, round_number):
    """Controla el turno de la máquina"""

    def bet(combination):
        bet = False
        if round_number == 0:
            if combination in ("escalera real", "escalera color", "poker", "full", "color",
                               "escalera", "trio", "doble pareja"):
                bet = True
            elif combination == "pareja" and random.randint(1, 3) in (1, 2):
                bet = True
            elif combination == "carta alta" and random.randint(1, 4) in (1, 2):
                bet = True
        elif round_number == 1:
            if combination in ("escalera real", "escalera color", "poker", "full", "color",
                               "escalera"):
                bet = True
            elif combination in ("trio", "doble pareja") and random.randint(1, 3) in (1, 2):
                bet = True
            elif combination == "pareja" and random.randint(1, 4) in (1, 2):
                bet = True
            elif combination == "carta alta" and random.randint(1, 5) == 1:
                bet = True
        elif round_number == 2:
            if combination in ("escalera real", "escalera color", "poker", "full"):
                bet = True
            elif combination in ("color", "escalera") and random.randint(1, 5) in (1, 2, 3, 4):
                bet = True
            elif combination in ("trio", "doble pareja") and random.randint(1, 6) in (1, 2, 3):
                bet = True
            elif combination == "pareja" and random.randint(1, 6) in (1, 2):
                bet = True
            elif combination == "carta alta" and random.randint(1, 6) == 1:
                bet = True

        return bet

    show_cards(player_cards, community_cards, "Máquina", round_number)
    input("\nENTER para continuar...")
    system("cls")

    hand = machine_cards + community_cards
    if round_number == 0:
        hand = hand[:5]
    elif round_number == 1:
        hand = hand[:6]

    print(analyze_hand(hand))

    if bet(analyze_hand(hand)):
        return True
    else:
        return False


def player_play(player_cards, community_cards, round_number):
    """Controla el turno del jugador"""

    show_cards(player_cards, community_cards, "Jugador", round_number)

    if input("\n¿Desea seguir jugando? [Y/N]: ").lower() == "y":
        bet = True
    else:
        bet = False
    system("cls")

    return bet


def game(player_cards, machine_cards, community_cards):
    """Ejecuta el juego"""

    system("cls")
    round_number = 0

    while round_number != 3:

        machine_bet = machine_play(
            machine_cards, community_cards, player_cards, round_number)
        if not machine_bet:
            break

        player_bet = player_play(
            player_cards, community_cards, round_number)
        if not player_bet:
            break

        round_number += 1

    if not machine_bet:
        show_cards(player_cards, community_cards, "Fin de la mano", round_number=round_number,
                   machine_cards=machine_cards)
        print("\nLa máquina se ha retirado. ¡Ganaste la mano!")
    elif not player_bet:
        show_cards(player_cards, community_cards, "Fin de la mano", round_number=round_number,
                   machine_cards=machine_cards)
        print("\nTe has retidado, perdiste la mano")
    elif round_number == 3:
        show_cards(player_cards, community_cards, "Fin de la mano", round_number=round_number,
                   machine_cards=machine_cards)
        print("\nPROXIMAMENTE...")  # Definir forma de calcular el ganador


def main():
    """Ejecuta el programa entero"""

    # Asigno cartas al jugador, a la máquina y a la mesa
    # player_cards, machine_cards, community_cards = define_cards()

    # game(player_cards, machine_cards, community_cards)

    player_cards = ['[A♠]', '[7♣]']
    community_cards = ['[10♦]', '[5♠]', '[3♣]', '[2♦]', '[9♠]']

    # machine_cards = ['[A♥]', '[A♦]']

    # game(player_cards, machine_cards, community_cards)

    combination = analyze_hand(player_cards + community_cards)
    print(combination)


if __name__ == "__main__":
    main()
