# This demo requires PyWebIO v1.6+
from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *


# add an input field when user clicks the '+add' button
@use_scope('button_section', clear=True)
def add_new_from_button():
    put_radio('foo', options=['option_1', 'option_2', 'Add New'], label='add-on question')
    put_scope('radio_section')
    pin_on_change(['foo'], onchange=add_new_from_radio)


# add extra input fields when user checks the 'add new' radio button
@use_scope('radio_section', clear=True)
def add_new_from_radio(item_input):
    if item_input == 'Add New':
        put_input('new_1', label='new input invoked by radio button -1')
        put_input('new_2', label='new input invoked by radio button -2')


# just show pin values for demo purpose
# customize this function to save data to your backend
def save_data(pin):
    user_input_list = ['more_questions', 'foo', 'new_1', 'new_2'] 
    for k in user_input_list:
        put_text(k+': '+str(pin[k]))


def main():
    put_scope('button_section')
    put_input('more_questions', label='more questions')
    put_buttons(['Submit', '+add'], onclick=[lambda: save_data(pin), lambda: add_new_from_button()])


if __name__ == '__main__':
    start_server(main, debug=True, port=9999)
