#!/usr/bin/python

import requests
import json
import logging

import utils_asc as util


class AttentionScorePublisher(object):
    """publishes attention scores with timestamp and sessionid to external ClientsHandler application"""

    _TARGET_ADDRESS = "http://145.24.222.180:80/api/image"
    _KEY_TIMESTAMP = "timestamp"
    _KEY_SESSION_ID = "sessionid"
    _KEY_ATTENTIONSCORE = "attentionscore"
    _OK = 200

    def publish_results(self, attention_score, session_id, timestamp):
        """publishes the results to the ClientsHandler module as JSON payload if attention score is not None"""
        if attention_score is not None:
            post_body = json.dumps({self._KEY_TIMESTAMP: timestamp, self._KEY_SESSION_ID: session_id,
                                    self._KEY_ATTENTIONSCORE: attention_score})
            headers = {}
            headers["Content-Type"] = "application/json"
            response = requests.post(self._TARGET_ADDRESS, data=post_body, headers=headers)
            log_message = util.construct_log_message(session_id, util.LOG_ATTENTION_SCORE, attention_score)
            logging.info(log_message)
            self._log_response(response)
        else:
            logging.warning(util.LOG_ATTENTION_SCORE_PUBLISH_FAILED)

    def _log_response(self, response):
        """logs the ClientManager's reponse as error or info, based on the status message"""
        log_response = util.construct_log_message(response.text, response.status_code, response.reason)
        status_code = response.status_code
        if status_code == self._OK:
            logging.info(log_response)
        else:
            logging.error(log_response)
