from flask import Flask, render_template, request
from ruamel.yaml import YAML
from pathlib import Path
from defusedxml import ElementTree
from xml.etree.ElementTree import ParseError

app = Flask(__name__)
config = YAML(typ='safe').load(Path('config.yml'))


@app.route('/mail/config-v1.1.xml', methods=['GET'])
def thunderbird():
    return render_template('thunderbird.xml', email=None, **config)


@app.route('/Autodiscover/Autodiscover.xml', methods=['POST'])
def outlook():
    try:
        email = ElementTree.fromstring(request.data).findtext('Request/EMailAddress')
    except ParseError:
        email = None

    if email is None:
        return 'Invalid autodiscover XML.', 400

    return render_template('outlook.xml', email=email, **config)
