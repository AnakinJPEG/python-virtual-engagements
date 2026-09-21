import random

display_map = [{"A1":"_", "A2":"_", "A3":"_", "A4":"_", "A5":"_"}, #0
               {"B1":"_", "B2":"_", "B3":"_", "B4":"_", "B5":"_"}, #1
               {"C1":"_", "C2":"_", "C3":"_", "C4":"_", "C5":"_"}, #2
               {"D1":"_", "D2":"_", "D3":"_", "D4":"_", "D5":"_"}, #3
               {"E1":"_", "E2":"_", "E3":"_", "E4":"_", "E5":"_"}] #4

active_battlemap = [{"A1":"_", "A2":"_", "A3":"_", "A4":"_", "A5":"_"}, #0
                    {"B1":"_", "B2":"_", "B3":"_", "B4":"_", "B5":"_"}, #1
                    {"C1":"_", "C2":"_", "C3":"_", "C4":"_", "C5":"_"}, #2
                    {"D1":"_", "D2":"_", "D3":"_", "D4":"_", "D5":"_"}, #3
                    {"E1":"_", "E2":"_", "E3":"_", "E4":"_", "E5":"_"}] #4


def user_map():
    for row in display_map:
        for cell in row.values():
            print(cell, end=" ")
        print()

def cast_battleships(total_ships=3):
    placed = 0
    while placed != total_ships:
        row = random.choice(active_battlemap)
        cell = random.choice(list(row.keys()))
        if row[cell] == "_":    # Empty cell selected
            row[cell] = "X"
            placed += 1


def main():

    total_ships = int(input("Define ship count: "))
    cast_battleships(total_ships)

    # for a in active_battlemap:
    #     for v in a.values():
    #         print(v, end=" ")
    #     print()

    discovered = 0
    miss_count = 0

    while True:
        user_map()
        guess = input("Take a guess [A1-E5]: ").upper()

        for row in active_battlemap:
            for key, value in row.items():
                if guess == key:
                    if value == "X":
                        print("Hit!")
                        discovered += 1
                    else:
                        print("Miss!")
                        miss_count += 1

                    row_index = active_battlemap.index(row)
                    display_map[row_index][key] = "X" if value == "X" else "0"

        if discovered == total_ships:
            print("YOU WIN!!!")
            print(f"Your miss count is: {miss_count}")
            if miss_count == 0:
                print("You're a great deal!")
            break





if __name__ == "__main__":
    main()
