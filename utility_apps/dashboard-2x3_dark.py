from pywebio import *
from pywebio.output import *
from pywebio.pin import *

img_link = "https://www.influxdata.com/wp-content/uploads/histogram.png"
md = '*Welcome, here is an instruction.....*'

def gdp_chart(plot_type):
    import plotly.express as px

    df = px.data.gapminder()
    fig = px.line_geo(df.query('year == 2007'), locations='iso_alpha', 
        color='continent', projection='orthographic', template="plotly_dark", )
    fig.update_layout(showlegend=False)
    
    animation = px.scatter(df, x='gdpPercap', y='lifeExp', color='continent', size='pop', size_max=40, 
                hover_name='country', template="plotly_dark", log_x=True, animation_frame='year',
                 animation_group='country', range_x=[100, 50000], range_y=[20,90])
                 
    if plot_type == 'animation':
        #put_html(gdp_chart('animation')) #put the plot on a pywebio app
        return animation.to_html(include_plotlyjs="require", full_html=True)
    elif plot_type == 'geo':
        #put_html(gdp_chart('geo')) #put the plot on a pywebio app
        return fig.to_html(include_plotlyjs="require", full_html=True)

@config(theme='dark')
def main():
    session.set_env(title='My Chart!!', output_max_width='90%')
    put_grid([
        [span(put_markdown('## Section A'), col=3)],
        [put_markdown('### Chart 1'), put_markdown('### Chart 2'), put_markdown('### Chart 3')],
        [put_markdown(md), put_scope('1-2'), put_scope('1-3')],
        [span(put_markdown('## Section B'), col=2, row=1), put_markdown('## Section C')],
        [span(put_row([
                put_select('x', help_text='X column', options=['a', 'b']),
                put_select('y', help_text='Y column', options=['x', 'y']),
                ]), col=2, row=1),
            None, 
        ],
        [span(put_image(img_link), col=2, row=1), put_scope('2-3')],
    ], cell_widths='33% 33% 33%')

    with use_scope('1-2'):
        put_html(gdp_chart('animation'))
        
    with use_scope('1-3'):
        put_html(gdp_chart('geo'))
        
    with use_scope('2-3'):
        put_markdown(md)
        put_input('something', label='input something to show as a toast message')
        put_button('submit', onclick=lambda: toast(pin.something))


if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
