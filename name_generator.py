from pywebio import *
from pywebio.output import *
from pywebio.input import *

def generate_name(car_info):
    '''
    Customized algorithm used to genearte a name (type: str) from input data (type: dict)
    This demo implements a very simple naming rule.
    '''
    if car_info['year'] >= 2020:
        return 'Golden Retriever'
    else:
        return 'Labrador'


def main():
    '''
    The function that runs as a PyWeb app
    Use this to define web components and user interaction logic
    '''
    #Header section
    put_markdown('# 🚗 Generate a nickname for your car')
    put_markdown('> Made with ❤️ by PyWeb.io')
    
    #The form for users to fill in
    car_info = input_group("Select all that match your car",[
      #input box component: func input()
      input('---Car maker---', name='maker'),
      
      #drop-down selection component: func select()
      select('---Select year (Required)---', options=[2021, 2020, 2019, 2018], name='year'),
      
      #checkbox component: func checkbox() 
      checkbox('---Who drives it---', options=['Mom', 'Dad', 'Alice', 'Bob'], inline=True, name='engine'),
      
      #radio button component: func radio()
      radio('---Color(Required)---', options=['Red', 'Blue', 'Black', 'Other'], required=True, inline=True, name='color'),
      
      #file uploading component: func file_upload()
      file_upload('---Upload a picture---', accept=['.jpg', '.png'], 
                  help_text='Only accept jpg and png formats. Your file is not uploaded to our server in this demo.', name='picture')
    ])
    
    #Generate car name based on user inputs
    car_name = generate_name(car_info)
    
    #Display the name on the web app
    put_markdown(' ### Your car\'s new nick name: `%s`' % car_name)
    
    #A counter for how many code names have been generated by users
    #A local file is used to store the count.
    with open('__name_generator_counter.txt', 'a+') as fp:
        fp.seek(0)
        count = fp.read()
        if not count: count = 0
        count = int(count) + 1
        fp.seek(0)
        fp.truncate()
        fp.write(str(count))

    #Display tool usage stats
    put_markdown('> %s nick names has been generated using this tool so far. [Generate one for another car](https://pyweb.io/app/58817/).' % count)
    
    #Add a section to collect user feedback.
    textarea('Tell us how to improve the tool', help_text='Please share with us what other features you like to see.')
    toast('Thanks for submitting your feedback!')
    
