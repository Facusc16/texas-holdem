"""Módulo para simular partida de Texas Holdem"""

import random
from os import system
import re

# Masos de cartas
value_deck = [[], [], [], [], [], [], [], [], [], [], [], [], []]
for i, value in enumerate(("A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2")):
    for suit in "♥♦♠♣":
        value_deck[i].append(f"[{value}{suit}]")

deck = sum(value_deck, [])

# Combinaciones de cartas
combination = ["escalera_real", "escalera_color", "poker", "full", "color", "escalera", "trio",
               "doble_pareja", "pareja", "carta_alta"]


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
    """Imprime en pantalla las cartas en juego"""

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

            if ("5" in sorted_hand[0] and "A" not in sorted_hand[4]
                    and ("A" in [card[1:2] for card in sorted_hand])):

                for i, card in enumerate(sorted_hand):
                    if "A" in card:
                        add = card
                        sorted_hand.pop(sorted_hand.index(card))
                        sorted_hand.insert(4, add)
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

    # Ordena la mano por valor más alto, o intenta armar una escalera
    if "highest" in priority:
        sorted_hand = highest(hand, priority)

    # Ordena la mano por palo
    elif priority == "suit":
        sorted_hand = suit(hand)

    # Ordena la mano por valor
    elif priority == "value":
        sorted_hand = value(hand)

    return sorted_hand


def analyze_hand(hand):
    """Devuelve las características de la mano"""

    def get_values(hand):
        return [n.replace("10", "1") for card in hand
                for n in re.findall(r"\[(\d{1,2}|[JQKA])", card)]

    def straight_combination(hand, flush=False):
        if flush == False:
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

    def flush_combination(hand):
        hand = sort_hand(hand, priority="suit")

        reference = None
        for card in hand[:5]:
            if reference is None:
                reference = card[-2]
            elif reference != card[-2]:
                return False

        flush_value = get_values(hand)

        return "color " + "".join(flush_value[:5])

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

        hand_values = get_values(hand)
        hand_values = hand_values[:5]

        if len(group_1) == 4:
            return f"poker {hand_values[0]}{hand_values[-1]}"

        elif len(group_1) == 3 and len(group_2) == 2:
            return f"full {hand_values[0]}{hand_values[3]}"

        elif len(group_1) == 3 and len(group_2) < 2:
            return f"trio {hand_values[0]}" + "".join(hand_values[3:])

        elif len(group_1) == 2 and len(group_2) == 2:
            return f"doble_pareja {hand_values[0]}{hand_values[2]}{hand_values[-1]}"

        elif len(group_1) == 2 and len(group_2) < 2:
            return f"pareja {hand_values[0]}" + "".join(hand_values[2:])

    # Verifica si la mano forma color
    if (flush := flush_combination(hand)):

        # Verifica si la mano forma escalera real, escalera color, o solo color
        if (straight := straight_combination(sort_hand(hand, priority="suit"), flush=True)):
            if straight[-1] == "A":
                return straight[:8] + "_real A"
            else:
                return straight[:8] + "_" + flush[:7]
        else:
            return flush

    # Verifica si la mano forma escalera
    elif (straight := straight_combination(hand)):
        return straight

    # Verifica si la mano forma poker, full, trio, doble pareja o pareja
    elif (value := value_combination(hand)):  # pylint: disable=redefined-outer-name
        return value

    # Determina que la mano solo tiene carta alta
    else:
        hand_values = get_values(hand)

        return "carta_alta " + "".join(hand_values[:5])


def find_index(lista, string):
    "Devuelve el índice de la carta en value_deck"

    for i, card in enumerate(lista):  # pylint: disable=redefined-outer-name
        for value in card:  # pylint: disable=redefined-outer-name
            if string in value:
                return i


def winning_card(machine_bet, player_bet, value_deck, indices, code):  # pylint: disable=redefined-outer-name
    "Encuentra la carta ganadora de la mano, o define empate"

    for i in indices:  # pylint: disable=redefined-outer-name

        tie_break_machine = find_index(value_deck, machine_bet[i])
        tie_break_player = find_index(value_deck, player_bet[i])

        if tie_break_machine < tie_break_player:
            if code == "1":
                machine_hand = machine_bet.replace("_", " ")
                player_hand = player_bet.replace("_", " ")
                salida = f"\nGana la máquina con {machine_hand} sobre {player_hand}"

            elif code == "2":
                machine_hand = machine_bet[:indices[0] + 1].replace("_", " ")
                player_hand = player_bet[:indices[0] + 1].replace("_", " ")
                salida = f"\nGana la máquina con {machine_hand} sobre {player_hand}"

                if i != indices[0]:
                    salida += f"\nKicker: {machine_bet[i]} sobre {player_bet[i]}"

            elif "3" in code:
                machine_hand = machine_bet[:indices[0] + 1].replace(
                    "_", " ") + "-" + machine_bet[indices[1]]
                player_hand = player_bet[:indices[0] + 1].replace(
                    "_", " ") + "-" + player_bet[indices[1]]
                salida = f"\nGana la máquina con {machine_hand} sobre {player_hand}"

                if code == "3a" and i == indices[2]:
                    salida += f"\nKicker: {machine_bet[i]} sobre {player_bet[i]}"

            elif code == "4":
                machine_hand = machine_bet[:5]
                player_hand = player_bet[:5]

                salida = f"\nGana la máquina con {machine_hand} sobre {player_hand}"
                salida += f"\nCarta alta: {machine_bet[i]} sobre {player_bet[i]}"

            if "1" in salida:
                salida = salida.replace("1", "10")

            return salida

        elif tie_break_player < tie_break_machine:
            if code == "1":
                machine_hand = machine_bet.replace("_", " ")
                player_hand = player_bet.replace("_", " ")
                salida = f"\nGanaste la mano con {player_hand} sobre {machine_hand}"

            elif code == "2":
                machine_hand = machine_bet[:indices[0] + 1].replace("_", " ")
                player_hand = player_bet[:indices[0] + 1].replace("_", " ")
                salida = f"\nGanaste la mano con {player_hand} sobre {machine_hand}"

                if i != indices[0]:
                    salida += f"\nKicker: {player_bet[i]} sobre {machine_bet[i]}"

            elif "3" in code:
                machine_hand = machine_bet[:indices[0] + 1].replace(
                    "_", " ") + "-" + machine_bet[indices[1]]
                player_hand = player_bet[:indices[0] + 1].replace(
                    "_", " ") + "-" + player_bet[indices[1]]
                salida = f"\nGanaste la mano con {player_hand} sobre {machine_hand}"

                if code == "3a" and i == indices[2]:
                    salida += f"\nKicker: {player_bet[i]} sobre {machine_bet[i]}"

            elif code == "4":
                machine_hand = machine_bet[:5]
                player_hand = player_bet[:5]

                salida = f"\nGanaste la mano con {player_hand} sobre {machine_hand}"
                salida += f"\nCarta alta: {player_bet[i]} sobre {machine_bet[i]}"

            if "1" in salida:
                salida = salida.replace("1", "10")

            return salida

    return f"\nEmpate de {machine_bet[:machine_bet.find(" ")].replace("_", " ")}"


def machine_play(machine_cards, community_cards, player_cards, round_number):
    """Turno de la máquina"""

    def bet(combination):  # pylint: disable=redefined-outer-name
        combination = combination[:combination.find(" ")]
        bet = False
        if round_number == 0:
            if combination in ("escalera_real", "escalera_color", "poker", "full", "color",
                               "escalera", "trio", "doble_pareja"):
                bet = True
            elif combination == "pareja" and random.randint(1, 3) in (1, 2):
                bet = True
            elif combination == "carta_alta" and random.randint(1, 4) in (1, 2):
                bet = True
        elif round_number == 1:
            if combination in ("escalera_real", "escalera_color", "poker", "full", "color",
                               "escalera"):
                bet = True
            elif combination in ("trio", "doble_pareja") and random.randint(1, 3) in (1, 2):
                bet = True
            elif combination == "pareja" and random.randint(1, 4) in (1, 2):
                bet = True
            elif combination == "carta_alta" and random.randint(1, 5) == 1:
                bet = True
        elif round_number == 2:
            if combination in ("escalera_real", "escalera_color", "poker", "full"):
                bet = True
            elif combination in ("color", "escalera") and random.randint(1, 5) in (1, 2, 3, 4):
                bet = True
            elif combination in ("trio", "doble_pareja") and random.randint(1, 6) in (1, 2, 3):
                bet = True
            elif combination == "pareja" and random.randint(1, 6) in (1, 2):
                bet = True
            elif combination == "carta_alta" and random.randint(1, 6) == 1:
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

    if bet((combination := analyze_hand(hand))):  # pylint: disable=redefined-outer-name
        return combination  # pylint: disable=redefined-outer-name


def player_play(player_cards, community_cards, round_number):  # Sacar comentarios
    """Turno del jugador"""

    show_cards(player_cards, community_cards, "Jugador", round_number)

    if input("\n¿Desea seguir jugando? [Y/N]: ").lower() == "y":

        hand = player_cards + community_cards
        if round_number == 0:
            hand = hand[:5]
        elif round_number == 1:
            hand = hand[:6]

        system("cls")
        return analyze_hand(hand)

    system("cls")


def game(player_cards, machine_cards, community_cards):
    """Ejecuta el juego"""

    system("cls")
    round_number = 0

    # Empieza la partida
    player_bet = None
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

    # Verifico si alguno de los jugadores decidió abandonar la mano
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

        # Verifico si alguno de los jugadores tiene una mano más alta que la otra
        if (combination.index(machine_bet[:machine_bet.find(" ")]) <
                combination.index(player_bet[:player_bet.find(" ")])):
            print(f"\nGana la máquina con {machine_bet[:machine_bet.find(" ")].replace("_", " ")}" +
                  f" sobre {player_bet[:player_bet.find(" ")].replace("_", " ")}")

        elif (combination.index(player_bet[:player_bet.find(" ")]) <
              combination.index(machine_bet[:machine_bet.find(" ")])):
            print(f"\nGanaste la mano con {player_bet[:player_bet.find(" ")].replace("_", " ")}" +
                  f" sobre {machine_bet[:machine_bet.find(" ")].replace("_", " ")}")

        # Verifico que combinación es más alta, o tiene el kicker más alto, o si empatan.
        else:
            if (machine_bet[:machine_bet.find(" ")] in
                    ("escalera_real", "escalera_color", "escalera")):
                print(winning_card(machine_bet, player_bet,
                                   value_deck, [-1], "1"))

            elif machine_bet[:machine_bet.find(" ")] == "color":
                print(winning_card(machine_bet, player_bet,
                      value_deck, [-5, -4, -3, -2, -1], "4"))

            elif machine_bet[:machine_bet.find(" ")] == "poker":
                print(winning_card(machine_bet,
                      player_bet, value_deck, [6, -1], "2"))

            elif machine_bet[:machine_bet.find(" ")] == "full":
                print(winning_card(machine_bet,
                      player_bet, value_deck, [5, -1], "3"))

            elif machine_bet[:machine_bet.find(" ")] == "trio":
                print(winning_card(machine_bet,
                      player_bet, value_deck, [5, 6, 7], "2"))

            elif machine_bet[:machine_bet.find(" ")] == "doble_pareja":
                print(winning_card(machine_bet,
                      player_bet, value_deck, [-3, -2, -1], "3a"))

            elif machine_bet[:machine_bet.find(" ")] == "pareja":
                print(winning_card(machine_bet,
                      player_bet, value_deck, [-4, -3, -2, -1], "2"))

            elif machine_bet[:machine_bet.find(" ")] == "carta_alta":
                print(winning_card(machine_bet, player_bet,
                      value_deck, [-5, -4, -3, -2, -1], "2"))


def main():
    """Ejecuta el programa entero"""

    # Asigno cartas al jugador, a la máquina y a la mesa
    player_cards, machine_cards, community_cards = define_cards()

    game(player_cards, machine_cards, community_cards)


if __name__ == "__main__":
    main()
