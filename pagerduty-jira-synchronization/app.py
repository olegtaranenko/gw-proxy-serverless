import json

from flask import Flask, jsonify, request

import webhooks


app = Flask(__name__)


@app.route("/pagerduty-webhook", methods=["POST"])
def pagerduty_webhook():
    webhooks.pagerduty(request.json)
    return jsonify({
        'ok': True,
    })
