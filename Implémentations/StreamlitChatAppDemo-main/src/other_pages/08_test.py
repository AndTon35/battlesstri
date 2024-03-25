import streamlit as st
import pandas as pd
import random

# Constants
BOARD_SIZE = 10
SHIP_SIZES = {'Carrier': 5, 'Battleship': 4, 'Destroyer': 3, 'Submarine': 2}

def create_board():
    # Create a DataFrame with columns labeled from A to J
    columns = [chr(65 + i) for i in range(BOARD_SIZE)]
    return pd.DataFrame([['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)], columns=columns)

def place_ship(board, row, col, length, direction, ship_name):
    if direction == "left":
        if col - length < 0:
            return False
        for i in range(length):
            if board.iloc[row, col - i] != '.':
                return False
        for i in range(length):
            board.iloc[row, col - i] = ship_name[0]
    elif direction == "right":
        if col + length >= BOARD_SIZE:
            return False
        for i in range(length):
            if board.iloc[row, col + i] != '.':
                return False
        for i in range(length):
            board.iloc[row, col + i] = ship_name[0]
    elif direction == "up":
        if row - length < 0:
            return False
        for i in range(length):
            if board.iloc[row - i, col] != '.':
                return False
        for i in range(length):
            board.iloc[row - i, col] = ship_name[0]
    elif direction == "down":
        if row + length >= BOARD_SIZE:
            return False
        for i in range(length):
            if board.iloc[row + i, col] != '.':
                return False
        for i in range(length):
            board.iloc[row + i, col] = ship_name[0]
    return True

def place_ships(board):
    for ship_name, ship_size in SHIP_SIZES.items():
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            direction = random.choice(["left", "right", "up", "down"])
            if place_ship(board, row, col, ship_size, direction, ship_name):
                break

def main():
    st.title("Battleship Game")
    st.write("Welcome to the Battleship game!")
    st.write("Your main objective is to find and destroy all the hidden ships on the map!")
    st.write("You have 10 ammo and there are 3 hidden ships on the map.")
    st.write("In order to hit them, you have to enter specific numbers for that location.")
    st.write("For example, for the first row and first column, you have to write 1 and A.")
    st.write("I wish you good fortune in wars to come!")

    board = create_board()
    place_ships(board)
    st.dataframe(board)

if __name__ == "__main__":
    main()
