from flask import Flask, render_template, request, redirect
from ruamel.yaml import YAML
from pathlib import Path
import re

app = Flask(__name__)
config = YAML(typ='safe').load(Path('config.yml'))


@app.errorhandler(404)
def redirect_to_lower(error):
    if request.url.islower():
        return error, 404
    return redirect(request.url.lower(), 308)


@app.route('/mail/config-v1.1.xml', methods=['GET'])
def thunderbird():
    return render_template('thunderbird.xml', **config)


@app.route('/autodiscover/autodiscover.xml', methods=['POST'])
def outlook():
    email = re.search(r'<EMailAddress>(.+)</EMailAddress>', request.data.decode('UTF8'))
    if email is None:
        return 'Invalid autodiscover XML.', 400
    email = email[1]

    return render_template('outlook.xml', email=email, **config)
