#live demo: https://demo.pyweb.io/first-project/grid_board/

from pywebio import *
from pywebio.output import *
from pywebio.input import *
from functools import partial

#define table size
grid_w = 5
grid_h = 9

#style table cell dimensions
cell_w = '100px'
cell_h = '100px'

#construct cell value in a list: [x cordinate, y cordinate, 'text shown in the cell', 'text shown in the popup window']
#Note: x, y start from 0, 0
_cells = [
    [0, 0, 'test 0 0', 'pop_up_text 0 0  '],
    [2, 3, 'test 2 3', 'pop_up_text 2 3'],
    [2, 5, 'test 2 5', 'pop_up_text 2 5'],
    [4, 8, 'test 4 8', 'pop_up_text 4 8'],
]

#pop up instruction with 2 buttons to label each test fail or pass
def popup_instruction(cell):
    with popup('Record test result') as s:
        put_markdown(cell[3])
        put_buttons(['Pass', 'Fail'], onclick=partial(put_result, cell=cell))

#display result back to the cell
def put_result(result, cell):
    with use_scope('%s-%s'%(cell[0],cell[1]), clear=True):
        if result == 'Pass':
            put_text("%s" % cell[2]).style('background: green').onclick(partial(popup_instruction, cell))
        elif result == 'Fail':
            put_text("%s" % cell[2]).style('background: red').onclick(partial(popup_instruction, cell))
    close_popup()


def main():

    #Display an empty grid with designated height and width, each cell is defined as a scope
    put_grid([[put_scope('%s-%s'%(x,y)).style('border: 1px groove;') for x in range(grid_w)] for y in range(grid_h)],
        cell_width=cell_w, cell_height=cell_h
    )

    #Add content to each cell
    for cell in _cells:
        put_text(cell[2], scope='%s-%s'%(cell[0],cell[1])).onclick(partial(popup_instruction, cell))
    
    put_link('Source code', '')
