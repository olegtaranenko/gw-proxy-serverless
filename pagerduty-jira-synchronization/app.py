import json
import logging

from flask import Flask, jsonify, request

import webhooks


app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route("/pagerduty-webhook", methods=["POST"])
def pagerduty_webhook():
    result = webhooks.pagerduty(request.json)
    return jsonify({
        'ok': result,
    })

@app.route("/pagerduty-webhook", methods=["POST"])
def pagerduty_webhook():
    response = {'ok': True}
    try:
        webhooks.pagerduty(request.json)
    except Exception as e:
        logger.exception(
            'Error occured during processing of a PagerDuty webhook')
        response = {
            'ok': False,
            'error': repr(e),
        }
    return jsonify(response)
