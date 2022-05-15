import logging
from docarray import Document
from pywebio import session, config, start_server
from pywebio.output import *
from pywebio.pin import *
import os, io, uuid
from discord import Webhook, RequestsWebhookAdapter, Embed, File
import urllib.parse

os.environ["DISCORD_WEBHOOK"] = 'https://discord.com/api/webhooks/974727187385159780/kzF5NJJIbJ1CR_jUMYc1IoW-_reQtX5FSC2CWClR2blBM-C2oHFURWcESA7745j7lah3'

_discord_webhook_url = os.environ["DISCORD_WEBHOOK"]
_webhook = Webhook.from_url(_discord_webhook_url, adapter=RequestsWebhookAdapter())
os.environ["JINA_HUB_ROOT"] = "/tmp/.jina"

server_url = 'grpc://dalle-flow.jina.ai:51005'

file_dir = os.path.dirname(os.path.abspath(__file__))

server_error_text = 'The demo server returned an error. Please come back in 5 mins and try again.'
image_gen_text = 'Generating images...\nThanks to JinaAI for providing the image generation service to public for free. This process may take up to 10 mins. Please be patient.'
step1 = "Step 1/3: Write down what you want to draw, and hit the `Draw` button. Up to 16 candidate images will be generated."
step2 = "Step 2/3: Click on your favorite image to fine tune it."
step3 = "Step 3/3: Choose one to generate a high-res image (1024 x 1024 px)"
credits = r'''### App source code:
https://github.com/pywebio/demos/tree/main/jina_dalle-flow

### Generated Art Gallery
Arts generated here are shared with PyWebIO community on our Discord server. Come see it: https://discord.gg/MvaCcg76Z7

**User privacy is fully respected as the sharing is anonymous.**

### Credits
This app is inspired by [JinaAI's DALL·E Flow project](https://github.com/jina-ai/dalle-flow): A Human-in-the-Loop workflow for creating HD images from text.

**JinaAI**
* [Dalle-flow](https://github.com/jina-ai/dalle-flow)
* [Clip as service](https://github.com/jina-ai/clip-as-service)

**Boris Dayma**
* [DALL·E Mini](https://github.com/borisdayma/dalle-mini)

**Jack Qiao**
* [Glid-3-xl](https://github.com/Jack000/glid-3-xl)

**Jingyun Liang**
* [SwinIR](https://github.com/JingyunLiang/SwinIR)
'''

def send_discord_result(prompt, image_data, stage):

    filename = uuid.uuid4().hex + '.png'
    file_path = os.path.join(file_dir, 'temp/', filename)
    
    if stage == 'preview':
        discord_msg = '🎨 New art has just been created on https://demo.pyweb.io/live/jina_dalle-flow/app/ from a text input: `' + prompt + '`\n'
    else:
        discord_msg = 'After fine-tuning, the final result of `' + prompt + ':`\n'
    
    msg = Embed(description=discord_msg, color=10312083)

    data = image_data.split(',')[1]
    b = urllib.parse.unquote_to_bytes(data)
    bo = io.BytesIO(b)

    with open(file_path, "wb+") as f:
        f.write(bo.getbuffer())

    with open(file_path, "rb") as f:
        my_file = File(f)
    
    _webhook.send(embed=msg)
    _webhook.send(file=my_file)


@use_scope('images', clear=True)
def upscale_gen(prompt, diffused, dfav_id):
    global server_url
    fav = diffused[dfav_id]
    send_discord_result(prompt, diffused[dfav_id, 'uri'], 'diffused')
    put_text(image_gen_text)
    try:
        with put_loading():
            fav = fav.post(f'{server_url}/upscale', target_executor='upscaler')
        clear()
        image_data = fav.uri
        put_image(image_data)
    except Exception as e:
        logging.exception(e)
        clear()
        popup(server_error_text)


@use_scope('images', clear=True)
def diffused_gen(prompt, da, fav_id):
    global server_url
    fav = da[fav_id]
    send_discord_result(prompt, da[fav_id, 'uri'], 'preview')
    put_text(image_gen_text)
    try:
        with put_loading():
            diffused = fav.post(f'{server_url}', parameters={'skip_rate': 0.5, 'num_images': 9},
                                target_executor='diffusion').matches
        clear()
        put_text(step3)
        for i in range(0, 9):
            image_data = diffused[i, 'uri']
            put_image(image_data).onclick(lambda x=i: upscale_gen(prompt, diffused, x))
    except Exception as e:
        logging.exception(e)
        clear()
        popup(server_error_text)


@use_scope('images', clear=True)
def preview_image_gen(prompt):
    global server_url
    if prompt.replace(" ", "") == '':
        toast('Please input a valid sentence', color='error', duration=10)
    else:
        put_text(image_gen_text)
        try:
            with put_loading():
                da = Document(text=prompt).post(server_url, parameters={'num_images': 8}).matches
            clear()
            put_text(step2)
            for i in range(0, 16):
                image_data = da[i, 'uri']
                put_image(image_data).onclick(lambda x=i: diffused_gen(prompt, da, x))
        except Exception as e:
            logging.exception(e)
            clear()
            popup(server_error_text)


css = """
#pywebio-scope-images {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-images:hover {
    overflow-y: scroll;
}
#pywebio-scope-input {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-input:hover {
    overflow-y: scroll;
}
/* Works on Firefox */
* {
  scrollbar-width: thin;
}
/* Works on Chrome, Edge, and Safari */
*::-webkit-scrollbar {
  width: 7px;
}
*::-webkit-scrollbar-track {
  background: transparent;
}
*::-webkit-scrollbar-thumb {
  background-color: gray;
  border-radius: 20px;
  border: 2px
}
"""

@config(theme="minty", css_style=css)
def main():
    session.set_env(title='Dall-E Flow Web App', output_max_width='100%')

    put_markdown('# Dall-E Flow Web App')
    put_row(
        [put_scope('input'), None, put_scope('images')],
        size="2fr 40px minmax(60%, 6fr)",
    )

    with use_scope('input'):
        put_textarea('description',
            placeholder='E.g., An oil painting of a humanoid robot playing chess in the style of Matisse',
            rows=5,
        ),
        put_button('Draw', onclick=lambda: preview_image_gen(pin['description']))
        put_markdown(credits).style('font-size: 12px; color: gray; background: #f6f6f6;')
    
    with use_scope('images'):
        put_markdown('### How it works')
        for step in [step1, step2, step3]:
            put_text(step)

if __name__ == '__main__':
    start_server(main, debug=True, port=9999)