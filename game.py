import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

#Create Players
class Player(NamedTuple):
    label: str
    color: str

#
class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

def tictactoe_grid(value):  
    print("\n")  
    print("\t      |      |")  
    print("\t    {} |  {}   |  {}".format(value[0], value[1], value[2]))  
    print('\t______|______|______')  
# printing the first three boxes of the 3X3 game board   
    print("\t      |      |") 
    print("\t   {}  |  {}   |  {}".format(value[3], value[4], value[5]))  
    print('\t______|______|______')  
    print("\t      |      |")  
# printing the second three boxes of the 3X3 game board   
    print("\t  {}   |  {}   |  {}".format(value[6], value[7], value[8]))  
    print("\t      |      |")  
    print("\n") 
# printing the last three boxes of the 3X3 game board   


class Game():
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self.players = cycle(players)
        self.board_size = board_size
        self.currentplayer = next(self.players)
        self.winning_combo = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        self._current_moves = []
    
    # value[chance - 1] = currentplayer  
    def _setup_board(self):
        self._current_moves = [
        [Move(row, col) for col in range(self.board_size)]
        for row in range(self.board_size)
    ]
        self.winning_combo = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]



    def winner():
        for i in self.winning_combo:  
        if all(j in current_player for j in i): 
            return True  
        return False     

    # def start():

    # def play_again():

    # def game_turn():

    # def game_manager():


class Gameboard():  


# #add a function called clearboard
# def clearboard():
    


# #add a function called is_take_place
# def is_take_place():
    


# #add a function called is_board_full
# def is_board_full():


# #add a function called is_game_won
# def is_game_won():



#add a function called print gameboard if statement to control the flow of the board
# def print_gameboard():

# def main():
#     """Create the game's board and run its main loop."""
#     game = TicTacToeGame()
#     board = Gameboard(board)
#     board.mainloop()

# if __name__ == "__main__":
#     main()


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = Game()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()