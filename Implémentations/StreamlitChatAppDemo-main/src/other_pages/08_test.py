import streamlit as st
import random
from itertools import product

# Constants
ROWS = 5
COLUMNS = 5
NUM_SHIPS = 3
GAME_COORDINATES = list(product(range(ROWS), range(COLUMNS)))

class Ship:
    def __init__(self):
        self.coord = (random.randint(0, ROWS-1), random.randint(0, COLUMNS-1))

    def __eq__(self, other):
        return self.coord == other

def create_game_board():
    return [["O" for _ in range(COLUMNS)] for _ in range(ROWS)]

def play_game():
    game_board = create_game_board()
    ships = set(Ship().coord for _ in range(NUM_SHIPS))
    ammo = 10

    while ammo:
        row = st.number_input("Enter a row number between 1-5 >: ", min_value=1, max_value=ROWS, value=1, step=1) - 1
        column = st.number_input("Enter a column number between 1-5 >: ", min_value=1, max_value=COLUMNS, value=1, step=1) - 1

        if game_board[row][column] == "-" or game_board[row][column] == "X":
            st.write("\nYou have already shot that place!\n")
            continue
        elif (row, column) in ships:
            st.write("\nBoom! You hit! A ship has exploded! You were granted a new ammo!\n")
            game_board[row][column] = "X"
            ships.remove((row, column))
            if not ships:
                st.write("My my, I didn't know you were a sharpshooter! Congratz, you won!")
                return
        else:
            st.write("\nYou missed!\n")
            game_board[row][column] = "-"
            ammo -= 1

        st.write(f"Ammo left: {ammo} | Ships left: {len(ships)}")
        st.write(game_board)

def main():
    st.title("Welcome to the Battleship game!")
    st.write("Your main objective is to find and destroy all the hidden ships on the map!")
    st.write("You have 10 ammo and there are 3 hidden ships on the map.")
    st.write("In order to hit them, you have to enter specific numbers for that location.")
    st.write("For example, for the first row and first column, you have to write 1 and 1.")
    st.write("I wish you good fortune in wars to come!")

    play_game()

if __name__ == "__main__":
    main()
