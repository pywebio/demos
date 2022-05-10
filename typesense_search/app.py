from pywebio import *
from pywebio.output import *
from pywebio.pin import *
from typesense import collection
import typesense
import string
import random


# Use your own config of typesense server
client = typesense.Client({
  'nodes': [{
    'host': '', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '',      # For Typesense Cloud use 443
    'protocol': ''   # For Typesense Cloud use https
  }],
  'api_key': '', #Add your own API key here
  'connection_timeout_seconds': 2
})


CURRENT_COLLECTION = 'companies'
SCHEMA = r'''
{
  "created_at": 1644964269,
  "default_sorting_field": "num_employees",
  "fields": [
    {
      "facet": false,
      "index": true,
      "name": "company_name",
      "optional": false,
      "type": "string"
    },
    {
      "facet": true,
      "index": true,
      "name": "num_employees",
      "optional": false,
      "type": "int32"
    },
    {
      "facet": true,
      "index": true,
      "name": "country",
      "optional": false,
      "type": "string"
    }
  ],
  "name": "companies",
  "num_documents": 4,
  "symbols_to_index": [],
  "token_separators": []
}'''


def uid_generator(size, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


@use_scope('dashboard', clear=True)
def put_schema():
    put_markdown('## Schema of `Companies`')
    put_code(SCHEMA, language='json')


@use_scope('results', clear=True)
def put_search_results(search_string=str(), query_by='company_name'):
    put_markdown('### Search Results for `%s` by `%s`'%(search_string, query_by))
    search_parameters = {
        'q'         : search_string,
        'query_by'  : query_by,
        'sort_by'   : '_text_match:desc'
    }
    if search_string != '':
        results = client.collections[CURRENT_COLLECTION].documents.search(search_parameters)
        for hit in results['hits']:
            put_html(hit['highlights'][0]['snippet'])
            for k,v in (hit['document']).items():
                put_code(k+': '+str(v))
            put_text('\n\n')

            
@use_scope('dashboard', clear=True)
def search_board():
    put_scope('search_box'),
    put_scope('results')

    with use_scope('search_box'):
        pin_list = [uid_generator(10), uid_generator(10)]
        put_row([
            put_input(name=pin_list[0], value='Air', help_text='Search String'), 
            None, 
            put_radio(name=pin_list[1], options=['company_name', 'country'], help_text='Query By', inline=True, value='company_name')
        ])
    pin_on_change(pin_list[0], onchange=lambda _: put_search_results(search_string=pin[pin_list[0]],query_by=pin[pin_list[1]]))
    pin_on_change(pin_list[1], onchange=lambda _: put_search_results(search_string=pin[pin_list[0]],query_by=pin[pin_list[1]]))


@use_scope('message')
def create_doc(name, emp_num, country):
    company = {
        "company_name": name,
        "num_employees": emp_num,
        "country": country        
    }
    try:
        client.collections[CURRENT_COLLECTION].documents.create(company)
        put_markdown('\n#### This document has been created successfully')
        for k,v in company.items():
            put_code(k+': '+str(v))
    except:
        toast('Something went wrong, sorry that the document has not been created')



@use_scope('dashboard', clear=True)
def add_document_board():
    put_row([put_scope('input'), 
        None, 
        put_scrollable(put_scope('message'), height=600, keep_bottom=True)
    ], size=('250px 30px 50%'))

    with use_scope('input'):
        put_markdown('### Create Single Document')
        put_input('name', label='Company Name')
        put_input('emp_num', label='Number of Employees', help_text='Number only', type='number')
        put_input('country', label='Country')
        put_button('Create', onclick=lambda: create_doc(pin.name, pin.emp_num, pin.country))

        put_markdown('\n\n----\n\n')
        put_markdown('### Batch Create Documents')
        put_button('File upload (UI only, backend function not implemented)', onclick=lambda _:(), disabled=True)


@config(theme='dark')
def main():
    session.set_env(title='TypeSense Search GUI Demo', output_max_width='100%')
    put_row([put_scope('left-navbar'), None, put_scope('dashboard')], size='200px 50px 85%')

    with use_scope('left-navbar'):
        put_grid([[
            put_text('TypeSense Search Gui Demo').style('background:#d90368; color:#ffffff; text-align: center; font-weight: bold; font-size: 15pt'),

            put_markdown('#### For End User'),
            put_markdown('- Search').onclick(lambda: search_board()),

            put_markdown('#### For Admin'),
            put_markdown('- Check Schema').onclick(lambda: put_schema()),
            put_markdown('- Add New Record').onclick(lambda: add_document_board()),

            put_markdown('----'),

            put_input('email',placeholder='your email'),
            put_button('Subscribe for Updates', color='success', small=True, onclick=lambda: toast('Got it!')),
        ]], direction='column')
    
    search_board()

if __name__ == '__main__':
    start_server(main, port=8888, debug=True)
