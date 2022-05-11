from docarray import Document
from pywebio import session, config, start_server 
from pywebio.output import *
from pywebio.pin import *
import os

os.environ["JINA_HUB_ROOT"] = "/tmp/.jina" 

server_url = 'grpc://dalle-flow.jina.ai:51005'

md = r'''Based on [JinaAI's DALL·E Flow project](https://github.com/jina-ai/dalle-flow): A Human-in-the-Loop workflow for creating HD images from text.
### How it works:
* Step 1: Write down what you want to draw, and hit the `Draw` button.
* Step 2: Up to 16 candidate images are generated. Click on one of them to fine tune it.
* Step 3: Another 9 images shows up. Click on your favorite one to generate a high-res image (1024 x 1024px).
* Step 4: Your art is ready to download and share. 

Note: If don't like what you see, simply re-draw a new batch. Enjoy creating!
'''

credits = r'''### App source code:
https://github.com/pywebio/demos/tree/main/jina_dalle-flow

### Credits

JinaAI
* [**Dalle-flow**](https://github.com/jina-ai/dalle-flow)
* [Clip as service](https://github.com/jina-ai/clip-as-service)

Boris Dayma
* [DALL·E Mini](https://github.com/borisdayma/dalle-mini)

Jack Qiao
* [Glid-3-xl](https://github.com/Jack000/glid-3-xl)

Jingyun Liang
* [SwinIR](https://github.com/JingyunLiang/SwinIR)
'''


@use_scope('images', clear=True)
def upscale_gen(diffused, dfav_id):
    global server_url
    fav = diffused[dfav_id]
    put_text('Generating images... (This process may take up to 2 mins. PLS be patient.)')
    try:
        with put_loading():
            fav = fav.post(f'{server_url}/upscale', target_executor='upscaler')
        clear()
        image_data = fav.uri
        put_image(image_data) 
    except:
        popup('The demo server returned an error. Please come back in 5 mins and try again.')


@use_scope('images', clear=True)
def diffused_gen(da, fav_id):
    global server_url
    fav = da[fav_id]
    put_text('Generating images... (This process may take up to 2 mins. PLS be patient.)')
    try:
        with put_loading():
            diffused = fav.post(f'{server_url}', parameters={'skip_rate': 0.5, 'num_images': 9}, target_executor='diffusion').matches
        clear()
        for i in range(0, 9):
            image_data = diffused[i, 'uri']
            put_image(image_data).onclick(lambda x=i: upscale_gen(diffused, x))
    except:
        popup('The demo server returned an error. Please come back in 5 mins and try again.')


@use_scope('images', clear=True)
def preview_image_gen(prompt):
    global server_url
    put_text('Generating images... (This process may take up to 4 mins. PLS be patient.)')
    try:
        with put_loading():
            da = Document(text=prompt).post(server_url, parameters={'num_images': 8}).matches
        clear()
        for i in range(0,16):
            image_data = da[i, 'uri']
            put_image(image_data).onclick(lambda x=i: diffused_gen(da, x))
    except:
        popup('The demo server returned an error. Please come back in 5 mins and try again.')



@config(theme="minty")
def main():
    session.set_env(title='Dall-E Flow Web App', output_max_width='100%')
    
    put_markdown('# Dall-E Flow Web App')
    put_row(
        [put_scope('left_navbar'), None, put_scope('page'), None, put_scope('credits').style('background: #f6f6f6')],
        size="2fr 40px 5fr 40px 1fr",
    )
    
    with use_scope('left_navbar'):
        put_markdown(md)
    
    with use_scope('page'):
        put_textarea('description', 
            placeholder='Art Description', 
            rows=3,
            help_text='E.g., An oil painting of a humanoid robot playing chess in the style of Matisse'
        ),
        put_button('Draw', onclick=lambda: preview_image_gen(pin['description']))
        put_scope('images')

    with use_scope('credits'):
        put_markdown(credits).style('font-size: 12px; color: gray')


if __name__ == '__main__':
    start_server(main, debug=True, port=9999)
