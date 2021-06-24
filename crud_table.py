from pywebio.output import *
from pywebio.input import *
from pywebio.session import *

from functools import partial

class CRUDTable():
    ''' 
    Generalizable Create, Read, Update, Delete Table class.
    :param gen_data_func: custom function that has procedure for generating the table data
    :param edit_func: custom function that edits, requires parameter "i" (index)
    :param del_func: custom function that deletes, requires parameter "i" (index)
    '''

    def __init__(self, gen_data_func, edit_func, del_func):
        
        self.datatable = gen_data_func()
        self.gen_data_func = gen_data_func
        self.edit_func = edit_func
        self.del_func = del_func
    
    def put_crud_table(self):

        # the CRUD table without the header
        table = []
        
        for i, table_row in enumerate(self.datatable):
            # skip the header row
            if i == 0:
                pass
            else:
                # full row of a table
                # get each row element of the data table row
                table_row = [put_text(row_element) for row_element in table_row] + [
                    # use i - 1 here so that it counts after the header row.
                    put_buttons(["◀️"], onclick=partial(self.handle_edit_delete, custom_func=self.edit_func,i=i)),
                    put_buttons(["✖️"], onclick=partial(self.handle_edit_delete, custom_func=self.del_func, i=i))
                ]              
                table.append(table_row)
        
        with use_scope("table_scope", clear=True):
            put_table(table,
                header= self.datatable[0] + ["Edit", "Delete"]
            )

    def handle_edit_delete(self, dummy, custom_func, i):
        '''when edit/delete button is pressed, execute the custom edit/delete
        function as well as update CRUD table'''

        # originally had it in the custom functions in step5_filemanager.py, 
        # but thought its probably best to have it within the crud_table class to
        # requery all the filepaths and refresh the crud_table
        
        if custom_func == self.edit_func:
        # if edit function, just do custom_func(i) without confirmation
            custom_func(i)
            # refresh table
            self.datatable = self.gen_data_func()
            self.put_crud_table()
        
        # if it's the delete function, ask for confirmation
        if custom_func == self.del_func:
            
            # melt the data (row becomes key, value)
            datatable_melt = list(zip(self.datatable[0], self.datatable[i+1]))

            popup(
                '⚠️ Are you sure you want to delete?',
                [
                    put_table(datatable_melt, header=["row", "data"]),
                    put_buttons(['confirm', 'cancel'], 
                    onclick = lambda x: self.handle_confirm(i) if x == 'confirm' else close_popup())
                ]
            )
    
    def handle_confirm(self, i):
        ''' if confirm button pressed in deletion confirmation, delete, and also close popup'''
        self.del_func(i)
        close_popup()
        
        # refresh table
        self.datatable = self.gen_data_func()
        self.put_crud_table()

sample_table = [
        ['Month', 'YouTube views', 'MoM growth'],
        ['2020-11', '167', '-'],
        ['2020-12', '233', '4%'],
        ['2021-01', '337', '200%'],
        ['2021-02', '440', '218%'],
        ['2021-03', '785', '15%'],
        ['2021-04', '6124', '174%'],
        ['2021-05', '88588', '1125%'],
        ['2021-05', '6500', '100%']
    ]


def generate_datatable():
    '''
    custom generate function to use for the CRUD table
    function for generating data.
    index 0 should be the headers.
    '''
    # datatable = [['header1', 'header2']] + data
    # here, data should be format [[row1col1,row1col2], [row2col1,row2col2]]
    # (notice that sublist size = 2 = # of header labels
    
    # I use [[filepath] for filepath... because pwl.find_blogfile() 
    # generates list of strings. doing list addition without [filepath] 
    # breaks strings and puts an alphabet in each table.
    
    return sample_table


def edit_table(i):
    '''
    custom edit function to use for the CRUD table
    load an old blog post, edit it
    '''
    sample_table[i][1] = input('input new view data for %s'% sample_table[i][0])
    
        
def delete_table(i):
    '''
    custom delete function to use for the CRUD table
    delete specific file
    '''
    sample_table.pop(i)


def main():

    '''CRUD table demo'''
    
    # Header
    # datatable = [header, row1, row2, row3] for the crud table
    growth_table = CRUDTable(gen_data_func=generate_datatable, edit_func=edit_table, del_func=delete_table)
    growth_table.put_crud_table()
    
    hold()
