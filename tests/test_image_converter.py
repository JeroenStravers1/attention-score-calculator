#!/usr/bin/python

import unittest
import os
import sys
import json
import os.path

sys.path.append("../src")

from image_converter import ImageConverter
import utils_asc as util

class ImageConverterTestSuite(unittest.TestCase):
    """contains tests for the image converter"""

    _KEY_TIMESTAMP = "timestamp"
    _KEY_SESSION_ID = "sessionid"
    _KEY_DATA = "data"
    _KEY_DATAURI = "frame"
    _KEY_CLIENT_ID = "clientid"

    _VALUE_TIMESTAMP = 10
    _VALUE_CLIENT_ID = "test_client_id"
    _VALUE_SESSION_ID = "test_session_id"
    _VALUE_DATAURI = "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAANAA0DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9zPCnxQ0vxb8ZfF/hzT/GXg/V7vwnaacmp+HbGRJNZ8O3FwJ5lkvds7FI7iDyDDG0EZAhmffKsiiLP/Zv+N2nfHHwJeTWerf2/qHhXVbvwpr2pQ+Hb7RLC71jT5DbagbOK73F7dbpJUDxzXEYaN4xPI0bmuP/AGmf2BPBv7SnxC0fx2mqeMPh78UfDtomnaZ448GasdM1mGyW9gvGsZwyyWt9ZvLAM219BcQgSSlUVpGauw/Zc/Zv0L9kj4E6H4A8O3niDVNP0b7RNLqWu6lJqWq6veXNxLdXl9d3EnMlxcXU888jAKu+Vtqou1QAf//Z"

    _IMG_EXTENSION = ".jpg"

    def setUp(self):
        self._provision_json_payload()
        image_converter = ImageConverter(self._simulated_json_payload)
        self._incoming_image_path = util.IMAGES_INCOMING + "/" + self._VALUE_SESSION_ID + "/" + self._VALUE_CLIENT_ID \
                                    + str(self._VALUE_TIMESTAMP) + self._IMG_EXTENSION
        self._stored_image_path = util.IMAGES_STORED + "/" + self._VALUE_SESSION_ID + "/" + self._VALUE_CLIENT_ID \
                                    + str(self._VALUE_TIMESTAMP) + self._IMG_EXTENSION

    def _provision_json_payload(self):
        """generate a json payload"""
        self._simulated_json_payload = json.dumps({
            self._KEY_TIMESTAMP: self._VALUE_TIMESTAMP,
            self._KEY_CLIENT_ID: self._VALUE_CLIENT_ID,
            self._KEY_SESSION_ID: self._VALUE_SESSION_ID,
            self._KEY_DATA: {
                self._KEY_DATAURI: self._VALUE_DATAURI
            }
        })

    def test_datauri_converted_to_image(self):
        """tests if the image converter successfully decoded the datauri in the json payload by checking if it stored
        an image named _VALUE_CLIENT_ID + _VALUE_TIMESTAMP + _IMG_EXTENSION in the 'images_stored' directory"""
        file_in_stored_dir = os.path.isfile(self._stored_image_path)
        self.assertTrue(file_in_stored_dir)

    def test_image_moved_from_incoming_to_stored(self):
        """tests if the image converter moved the decoded image from images_incoming to images_stored."""
        file_in_incoming_dir = os.path.isfile(self._incoming_image_path)
        self.assertFalse(file_in_incoming_dir)

    def tearDown(self):
        self._remove_test_image_converter_file_and_dirs()

    def _remove_test_image_converter_file_and_dirs(self):
        """remove the test image and dir created for test_image_transporter_file_transfer test"""
        dir_in_incoming = util.IMAGES_INCOMING + "/" + self._VALUE_SESSION_ID
        dir_in_stored = util.IMAGES_STORED + "/" + self._VALUE_SESSION_ID
        util.remove_dir(dir_in_incoming)
        util.remove_file(self._stored_image_path)
        util.remove_dir(dir_in_stored)
