from pywebio import *
from pywebio.output import *
from pywebio.input import *

from pywebio.session import *
import time

goboard_size = 15
# -1->none, 0 -> black, 1 -> white
goboard = [
    [-1] * goboard_size
    for _ in range(goboard_size)
]

def winner():  # return winner piece, return None if no winner
    for x in range(2, goboard_size - 2):
        for y in range(2, goboard_size - 2):
            # check if (x,y) is the win center
            if goboard[x][y] != -1 and any([
                all(goboard[x][y] == goboard[m][n] for m, n in [(x - 2, y), (x - 1, y), (x + 1, y), (x + 2, y)]),
                all(goboard[x][y] == goboard[m][n] for m, n in [(x, y - 2), (x, y - 1), (x, y + 1), (x, y + 2)]),
                all(goboard[x][y] == goboard[m][n] for m, n in [(x - 2, y - 2), (x - 1, y - 1), (x + 1, y + 1), (x + 2, y + 2)]),
                all(goboard[x][y] == goboard[m][n] for m, n in [(x - 2, y + 2), (x - 1, y + 1), (x + 1, y - 1), (x + 2, y - 2)]),
            ]):
                return ['⚫', '⚪'][goboard[x][y]]

session_id = 0
current_turn = 0
player_count = [0, 0]

def main():
    """Online Drop-in Gomoku Game

    A web based Gomoku (AKA GoBang, Five in a Row) game made with PyWebIO under 100 lines of Python code."""
    global session_id, current_turn, goboard
    if winner():  # The current game is over, reset game
        goboard = [[-1] * goboard_size for _ in range(goboard_size)]
        current_turn = 0

    my_turn = session_id % 2
    my_stone = ['⚫', '⚪'][my_turn]
    session_id += 1
    player_count[my_turn] += 1

    @defer_call
    def player_exit():
        player_count[my_turn] -= 1

    set_env(output_animation=False)
    
    put_html("""<style> table th, table td { padding: 0px !important;} button {padding: .75rem!important; margin:0!important} </style>""")  # Custom styles to make the board more beautiful

    put_markdown(f"""# Online Drop-in Gomoku Game
    In this Gomoku (AKA Gobang, Five in a Row) game, online players are assigned to two groups: black and white. All players have opportunities to place a stone on an empty intersection. Whoever makes the first move represents the group. The winner is the first group to form an unbroken chain of five stones horizontally, vertically, or diagonally. More hisotry about the game: https://en.wikipedia.org/wiki/Gomoku
    There're currently {player_count[0]} players for ⚫, {player_count[1]} for ⚪.
    Your role is {my_stone}.
    """, lstrip=True)

    def set_stone(pos):
        global current_turn
        if current_turn != my_turn:
            toast("It's not your turn!!", color='error')
            return
        x, y = pos
        goboard[x][y] = my_turn
        show_goboard()
        current_turn = (current_turn + 1) % 2

    @use_scope('goboard', clear=True)
    def show_goboard():
        table = [
            [
                put_buttons([dict(label=' ', value=(x, y), color='light')], onclick=set_stone) if cell == -1 else [' ⚫', ' ⚪'][cell]
                for y, cell in enumerate(row)
            ]
            for x, row in enumerate(goboard)
        ]
        put_table(table)

    show_goboard()
    while not winner():
        with use_scope('turn_status', clear=True):
            put_row([put_text("Your opponent's turn, waiting... "), put_loading().style('width:1.5em; height:1.5em')], size='auto 1fr')
            while current_turn != my_turn:  # wait your opponent to finish their move
                time.sleep(0.5)
            show_goboard()
            if winner():
                break
            clear()
            put_text("It's your turn!")
            while current_turn == my_turn:  # wait our group to finish current move
                time.sleep(0.5)
            show_goboard()
    show_goboard()
    clear('turn_status')
    put_text('Game over. The winner is %s!\nRefresh page to join a new round.' % winner())
