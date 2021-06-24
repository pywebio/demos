from pywebio import *
from pywebio.output import *
from pywebio.input import *

def main():
    put_markdown('# 🗃 Manufacturing Data Pre-processing')
    put_text('')
    
    input_group('Excel File Convertor', inputs=[
        input('Data source (manufacturer ID)', name='manufacturer'),
        input('Your name', name='username'),
        
        radio(label='Choose a format to convert to', 
        options=['CSV', 'JSON', 'Pandas DataFrame Object (Pickle dump)'], 
        inline=True, value='CSV', name='format'),

        file_upload(label='Upload manufacturing report', 
                    accept=['.xlsx', '.csv', '.xls', 'xlsm'],
                    max_size='10K',
                    help_text='Allowed formats: .csv, .xlsx, .xls, .xlsm. Max size: 10K',
                    name='file')
                    ])
                    
    popup('We got your file', [
        put_markdown('It has been processed. The new data file is saved in your shared folder.'),
        put_html('<button type="button" onClick="window.location.reload();">Convert another file</button>')
        ])
