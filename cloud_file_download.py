from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.session import hold 

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
    hold()
