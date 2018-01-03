import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '544027094:AAHEboUFRaa22mqgp8FR_pF06mips0hNiVs'
WEBHOOK_URL = 'https://6075bb75.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'listen1',
        'listen2',
	'rank',
	'hero',
	'time'
	
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'listen1',
            'conditions': 'is_going_to_listen1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'listen2',
            'conditions': 'is_going_to_listen2'
        },
	{
	    'trigger':'advance',
	    'source':'listen1',
	    'dest':'rank',
	    'conditions': 'is_going_to_rank'
	},
        {
            'trigger':'advance',
            'source':'listen2',
            'dest':'hero',
            'conditions': 'is_going_to_hero'
        },
        {
            'trigger':'advance',
            'source':'user',
            'dest':'time',
            'conditions': 'is_going_to_time'
        },
        {
            'trigger': 'go_back',
            'source': ['hero','rank','time'],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

#############################################################################
def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run(port=5000)
#############################################################################
