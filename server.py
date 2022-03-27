from flask import Flask, render_template, request
from ruamel.yaml import YAML
from pathlib import Path
import re

app = Flask(__name__)

config = YAML(typ='safe').load(Path('config.yml'))
for protocol in ['imap', 'smtp']:
    config[protocol]['encryption'] = {
        'outlook': 'on' if config[protocol]['mode'] in {'SSL', 'STARTTLS'} else 'off',
        'thunderbird': config[protocol]['mode'],
    }


@app.route('/mail/config-v1.1.xml', methods=['GET'])
def thunderbird():
    return render_template('thunderbird.xml', email=None, **config)


@app.route('/Autodiscover/Autodiscover.xml', methods=['POST'])
def outlook():
    email = re.search(r'<EMailAddress>(.+)</EMailAddress>', request.data.decode('UTF8'))
    if email is None:
        return 'Invalid autodiscover XML.', 400
    email = email[1]

    return render_template('outlook.xml', email=email, **config)
