#!/usr/bin/python

import unittest
import os
import sys
import hug
import json

sys.path.append("../src")

import api


class ApiTestSuite(unittest.TestCase):
    """contains tests for the HUG api"""

    _API_TEST_PULSE = "/pulse"
    _API_TEST_RESPONSE_200 = "200 OK"

    def test_api_response(self):
        """tests if the api returns 200 upon receiving a request"""
        test_pulse_response = hug.test.get(api, self._API_TEST_PULSE)
        self.assertTrue(test_pulse_response.status == self._API_TEST_RESPONSE_200)
