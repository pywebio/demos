from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *
from pywebio.session import hold

def put_pin_value(text):
    with use_scope('text_output', clear=True):
        put_text(text)

def main():
    put_table([
                ['Commodity', 'Price / unit'],
                ['Apple', '0.5'],
                ['Banana', '0.4'],
                ['Avacado', '1.2'],
            ])
            
    put_tabs([
        {'title': 'Search by fruit', 'content': [
            put_row(
                [put_input('fruit'),
                put_buttons(['search'], lambda _: put_pin_value(pin.fruit)),
            ], )
        ]},
        {'title': 'Search by price', 'content': [
            put_row(
                [put_input('price'),
                put_buttons(['search'], lambda _: put_pin_value(pin.price)),
            ], )
        ]},
        {'title': 'Help', 'content': 'Input a fruit name of interest then hit the search button.'},
    ])
    
    use_scope('text_output')
    hold()
