from pywebio import *
from pywebio.output import *
from pywebio.input import *

import plotly.express as px
import numpy as np

ALIVE = 1
DEAD = 0

def game_of_life(grid, steps):
    grid = np.array(grid)
    full_frame=np.stack((grid, grid))
    N, M = grid.shape
    
    for n in range(steps):
        newGrid = grid.copy()
        for i in range(N):
            for j in range(M):
                total = (grid[i, (j-1)%M] + grid[i, (j+1)%M] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%M] + grid[(i-1)%N, (j+1)%M] +
                         grid[(i+1)%N, (j-1)%M] + grid[(i+1)%N, (j+1)%M])
                if grid[i, j]  == ALIVE:
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = DEAD
                else:
                    if total == 3:
                        newGrid[i, j] = ALIVE
        if n == 0: 
            full_frame=np.stack((grid, newGrid))
        else: 
            full_frame = np.append(full_frame, np.array([newGrid.tolist()]), axis=0)
        grid = newGrid
    return full_frame

def check_array(string):
    cnt_list = []
    cnt  = 0
    for i in string:
        if i in ['0', '1']:
            cnt += 1
        elif i =='\n':
            cnt_list.append(cnt)
            cnt = 0
        else:
            return 'Only 0 and 1 are accepted for input'
    cnt_list.append(cnt)
    if len(set(cnt_list)) != 1:
        return 'All rows need to have the same length. Empty row cannot be accepted.'
    elif cnt == 0: return 'Empty row cannot be accepted'

@use_scope('example', clear=True)
def show_example(choice):
    if choice == 'Sample solution':
        put_code(solution_code, language='python', rows=20)
    if choice == 'Sample initial inputs': 
        put_scrollable(put_markdown(input_1), height=400)
    
def step_limit(n):
    if n <= 0: 
        return 'We cannot go back in time'
    elif n > 50: 
        return 'Please input a number < 50'

solution_code = r'''import numpy as np

ALIVE = 1
DEAD = 0

def game_of_life(grid, steps):
    grid = np.array(grid)
    N, M = grid.shape

    for n in range(steps):
        newGrid = grid.copy()
        for i in range(N):
            for j in range(M):
                total = (grid[i, (j-1)%M] + grid[i, (j+1)%M] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%M] + grid[(i-1)%N, (j+1)%M] +
                         grid[(i+1)%N, (j-1)%M] + grid[(i+1)%N, (j+1)%M])
                if grid[i, j]  == ALIVE:
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = DEAD
                else:
                    if total == 3:
                        newGrid[i, j] = ALIVE
        grid = newGrid

    return grid.tolist()
'''
description =r'''
This is a web app built to visualize [Project Lovelace's 'Game of Life' problem](https://projectlovelace.net/problems/game-of-life/)
Made on [pyweb.io](https://pyweb.io)

------------
### Click the buttons to see sample code or copy initial inputs to start your simulation
'''

input_1 = r'''
A bunch of still life patterns that do not change shape under the evolution rules, and some oscillator patterns that flip between the same patterns again and again ==>
000000000000000000000000000000000000
011000001100000000000000000000000000
011000010010000000000001110001110000
000000001010000011100000000000000000
000000000100000000000100001010000100
000110000000000000000100001010000100
001001000001000000000100001010000100
000110000010100000000001110001110000
000000000001000011100000000000000000
000000000000000111000001110001110000
011000000000000000000100001010000100
011000000000000000000100001010000100
000110000000000000000100001010000100
000110000000000000000000000000000000
000000000000000000000001110001110000
000000000000000000000000000000000000
000000000000000000000000000000000000


A glider gun pattern that generate gliders, which are spaceship patterns that move across the grid ==>
000000000000000000000000100000000000
000000000000000000000010100000000000
000000000000110000001100000000000011
000000000001000100001100000000000011
110000000010000010001100000000000000
110000000010001011000010100000000000
000000000010000010000000100000000000
000000000001000100000000000000000000
000000000000110000000000000000000000


Pulsar ==>
0011100011100
0000000000000
1000010100001
1000010100001
1000010100001
0011100011100
0000000000000
0011100011100
1000010100001
1000010100001
1000010100001
0000000000000
0011100011100
'''


def main():
    session.set_env(title='Game of Life Simulator')
    put_markdown('# ⚗️ Convey\'s game of life simulator' )
    put_markdown(description)

    put_buttons(['Sample solution', 'Sample initial inputs'], 
                onclick=show_example)
    
    data = input_group('Now, define your simulation and check the result', 
            [textarea('Input a 2D integer array representing the grid where the dead cells are represnted by 0\'s and the alive cells are 1\'s',
             required=True, placeholder='Please use this format:\n01010\n00101\n00101', 
             validate=check_array, name='input_grid'),
             input('How many steps you want to run the simulation', name='step', 
             required=True, type=NUMBER, validate=step_limit, 
             help_text='Input a number between 1 and 50')
             ])
       
    input_array = [[]]
    row = 0
    for i in data['input_grid']:
        if i !=  '\n':
            input_array[row].append(int(i))
        else:
            input_array.append([])
            row += 1

    final_array = game_of_life(input_array, data['step'])
    #put_text(final_array)
    
    fig = px.imshow(final_array, animation_frame=0, aspect='equal',
                    binary_string=True, zmin=0, zmax=1)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    

    put_html(fig.to_html(include_plotlyjs="require", full_html=False))
    
    put_markdown('## [Run another simulation](https://pyweb.io/app/34709/)')
    session.hold()


if __name__ == '__main__':
    start_server(main, debug=True, port=9999)