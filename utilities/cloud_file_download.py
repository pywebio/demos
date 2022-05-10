from pywebio import *
from pywebio.output import *
from pywebio.input import *

def main():
    #read file
    try: 
        with open ('__foo.ob', 'rb') as fp:
            content = fp.read()
    except IOError:
        with open('__foo.ob', 'w') as fp:
            content = 'Hello from PyWebIO'
            fp.write(content)
    
    put_file('download_filename.txt', content, 'download link')


if __name__ == '__main__':
    start_server(main, debug=True, port=9999)