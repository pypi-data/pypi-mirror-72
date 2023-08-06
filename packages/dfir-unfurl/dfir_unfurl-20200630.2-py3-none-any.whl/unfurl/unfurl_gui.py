
from flask import Flask, render_template, request, g
from flask_cors import CORS
import os
from unfurl import unfurl



class UnfurlApp:
    def __init__(self, unfurl_debug='True', unfurl_host='localhost', unfurl_port='5000'):
        self.unfurl_debug = unfurl_debug
        self.unfurl_host = unfurl_host
        self.unfurl_port = unfurl_port

        global uhost
        global uport
        uhost = unfurl_host
        uport = unfurl_port

        app.run(debug=unfurl_debug, host=unfurl_host, port=unfurl_port)


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    x = app
    return render_template(
        'graph.html', url_to_unfurl='', unfurl_host=uhost,
        unfurl_port=uport)


@app.route('/<path:url_to_unfurl>')
def graph(url_to_unfurl):
    return render_template(
        'graph.html', url_to_unfurl=url_to_unfurl,
        unfurl_host=uhost, unfurl_port=uport)


@app.route('/api/<path:api_path>')
def api(api_path):
    # Get the referrer from the request, which has the full url + query string.
    # Split off the local server and keep just the url we want to parse
    unfurl_this = request.referrer.split(f':{uport}/', 1)[1]

    unfurl_instance = unfurl.Unfurl()
    unfurl_instance.add_to_queue(
        data_type='url', key=None,
        extra_options={'widthConstraint': {'maximum': 1200}},
        value=unfurl_this)
    unfurl_instance.parse_queue()

    unfurl_json = unfurl_instance.generate_json()
    return unfurl_json

