from pywebio.output import *
from pywebio.input import *

def main():
    name = input('Tell us your name')
    put_text('Hello %s'%name)

if __name__ == '__main__':
    from pywebio.platform import start_server
    start_server(main, port=8089, debug=True)