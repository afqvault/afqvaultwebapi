# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import socket

from eve import Eve
from eve.auth import TokenAuth
from eve_swagger import swagger
from settings import settings
import json
import jwt
import datetime
from flask.json import jsonify

API_TOKEN = os.environ.get("API_TOKEN")


def on_insert_nodes(items):
    for i in items:
        # Convert encode string as json
        if isinstance(i['metrics'], str):
            i['metrics'] = json.loads(i['metrics'])


def on_insert_subjects(items):
    for i in items:
        # Convert encode string as json
        if isinstance(i['metadata'], str):
            i['metadata'] = json.loads(i['metadata'])


def on_insert_projects(items):
    for i in items:
        # Convert encode string as json
        if isinstance(i['scan_parameters'], str):
            i['scan_parameters'] = json.loads(i['scan_parameters'])


class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return token == API_TOKEN


app = Eve(settings=settings, auth=TokenAuth)
app.register_blueprint(swagger, url_prefix='/docs/api')
app.add_url_rule('/docs/api', 'eve_swagger.index')


@app.route('/api/socket_auth_token/<token>')
def socket_authenticate(token):
    if token != API_TOKEN:
        raise RuntimeError("DOES NOT MATCH")

    secret = app.config["SECRET_KEY"]  # self.cfg['app:secret-key']
    wstoken = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'username': token,
        }, secret)

    response = jsonify({"socktoken": wstoken})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/delete_project/<project_id>')
def delete_project(project_id):
    print("DELETING PROJECT ID", project_id)
    projects = app.data.driver.db['projects']
    subjects = app.data.driver.db['subjects']
    projects.remove({"_id": project_id})
    subjects.remove({"project_id": project_id})
    return jsonify({"status": 0})


@app.route('/api/authenticate/<provider>/<code>')
def authenticate(domain, provider, code):
    provider = provider.upper()
    data = {'client_id': app.config[provider+'_CLIENT_ID'],
            'client_secret': app.config[provider+'_CLIENT_SECRET'],
            'code': code}
    tr = requests.post(app.config[provider+'_ACCESS_TOKEN_URL'], data=data)
    print(tr.text)
    try:
        token = re.findall(app.config['TOKEN_RE'], tr.text)[0]
    except IndexError as e:
        return tr.text
    # TODO: use token to get members of the AFQ-Vault organization
    # and use token to get user info. If user in AFQ-Vault organization
    # return token. Else, return 401 unauthorized.
    token = bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()

    return jsonify({'token': token})


# required. See http://swagger.io/specification/#infoObject for details.
app.config['SWAGGER_INFO'] = {
    'title': 'AFQVault Web API',
    'version': 'v1',
    'description': """
    AFQVault description
    based on the mriqc api by
the <a href="http://cmn.nimh.nih.gov">Data Science and Sharing Team</a>
at the <a href="http://nimh.nih.gov">National Institute of Mental Health</a>.
""",
}

# app.config["SECRET_KEY"] = "anishaisgreat" this was for websockets

app.on_insert_nodes = on_insert_nodes
app.on_insert_subjects = on_insert_subjects
app.on_insert_projects = on_insert_projects

if __name__ == '__main__':
    app.run(host='0.0.0.0')
