import json
import logging

from flask import Flask, jsonify, request

import webhooks, jirawebhook


app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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


@app.route("/jira-webhook", methods=["POST"])
def jira_webhook():
    result = webhooks.jira(request.json)
    return jsonify({
        'ok': result,
    })

