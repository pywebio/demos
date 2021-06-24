from pywebio import *
from pywebio.output import *
from pywebio.input import *

import asyncio

from pywebio.session import defer_call, info as session_info, run_async

MAX_MESSAGES_CNT = 10 ** 4

chat_msgs = []  # (name, msg)
online_users = set() 


async def refresh_msg(my_name, msg_box):
    """send new message to current session"""
    global chat_msgs
    last_idx = len(chat_msgs)
    while True:
        await asyncio.sleep(0.5)
        for m in chat_msgs[last_idx:]:
            if m[0] != my_name:  # only refresh message that not sent by current user
                msg_box.append(put_markdown('`%s`: %s' % m, sanitize=True))

        # remove expired message
        if len(chat_msgs) > MAX_MESSAGES_CNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)


async def main():
    """A Chat room demo |
    You can chat with everyone currently online.
    """
    global chat_msgs

    put_markdown("## PyWebIO chat room\nWelcome to the chat room, you can chat with all the people currently online. You can open this page in multiple tabs of your browser to simulate a multi-user environment. This application uses less than 90 lines of code, the source code is [here](https://github.com/wang0618/PyWebIO/blob/dev/demos/chat_room.py)", lstrip=True)

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)
    nickname = await input("Your nickname", required=True, validate=lambda n: 'This name is already been used' if n in online_users or n == '📢' else None)

    online_users.add(nickname)
    chat_msgs.append(('📢', '`%s` joins the room. %s users currently online' % (nickname, len(online_users))))
    msg_box.append(put_markdown('`📢`: `%s` join the room. %s users currently online' % (nickname, len(online_users)), sanitize=True))

    @defer_call
    def on_close():
        online_users.remove(nickname)
        chat_msgs.append(('📢', '`%s` leaves the room. %s users currently online' % (nickname, len(online_users))))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group('Send message', [
            input(name='msg', help_text='Message content supports inline Markdown syntax'),
            actions(name='cmd', buttons=['Send', 'Multiline Input', {'label': 'Exit', 'type': 'cancel'}])
        ], validate=lambda d: ('msg', 'Message content cannot be empty') if d['cmd'] == 'Send' and not d['msg'] else None)
        if data is None:
            break
        if data['cmd'] == 'Multiline Input':
            data['msg'] = '\n' + await textarea('Message content', help_text='Message content supports Markdown syntax')
        msg_box.append(put_markdown('`%s`: %s' % (nickname, data['msg']), sanitize=True))
        chat_msgs.append((nickname, data['msg']))

    refresh_task.close()
    toast("You have left the chat room")
