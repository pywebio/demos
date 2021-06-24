from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.session import hold 

def main():
    #read a file
    with open ('__foo.ob', 'rb') as fp:
        content = fp.read()
    put_file('download_filename.ob', content, 'download link')
    hold()
