#!/usr/bin/python

import unittest
import os
import sys
import logging

sys.path.append("../src")
import utils_asc as util


class UtilLoggingTestSuite(unittest.TestCase):
    """contains tests for the head pose processor module"""

    _PATH_TO_TEST_DIR = "../tests"
    _ERROR_MESSAGE = "test_error"
    _INFO_MESSAGE = "test_info"
    _LOG_INFO_NAME = "asc_log_info.log"
    _LOG_ERRORS_NAME = "asc_log_errors.log"
    _TWO_FILES_CREATED = 2
    _TWO_FILES_REMOVED = 0

    def setUp(self):
        self._provision_test_util_logging()

    def _provision_test_util_logging(self):
        """initiate logging, log an error, log info"""
        util.initialize_logging(self._PATH_TO_TEST_DIR)
        logging.info(self._INFO_MESSAGE)
        logging.error(self._ERROR_MESSAGE)

    def test_log_file_creation(self):
        """check creation of log files"""
        info_log_created = os.path.isfile(self._PATH_TO_TEST_DIR + "/" + self._LOG_INFO_NAME)
        error_log_created = os.path.isfile(self._PATH_TO_TEST_DIR + "/" + self._LOG_ERRORS_NAME)
        files_created = info_log_created + error_log_created # devnote: booleans are 1 or 0, and a subclass of int
        self.assertTrue(files_created == self._TWO_FILES_CREATED)

    def test_info_log_file_info_content(self):
        """check if info log contains info message"""
        with open(self._PATH_TO_TEST_DIR + "/" + self._LOG_INFO_NAME, 'r') as info_log:
            log_content = info_log.read()
        self.assertTrue(self._INFO_MESSAGE in log_content)

    def test_info_log_file_error_content(self):
        """check if info log contains error message"""
        with open(self._PATH_TO_TEST_DIR + "/" + self._LOG_INFO_NAME, 'r') as info_log:
            log_content = info_log.read()
        self.assertTrue(self._ERROR_MESSAGE in log_content)

    def test_error_log_file_error_content(self):
        """check if error log contains error message"""
        with open(self._PATH_TO_TEST_DIR + "/" + self._LOG_ERRORS_NAME, 'r') as error_log:
            log_content = error_log.read()
        self.assertTrue(self._ERROR_MESSAGE in log_content)

    def test_error_log_file_info_content(self):
        """check if error log contains info message"""
        with open(self._PATH_TO_TEST_DIR + "/" + self._LOG_ERRORS_NAME, 'r') as error_log:
            log_content = error_log.read()
        self.assertFalse(self._INFO_MESSAGE in log_content)

    def tearDown(self):
        logging.shutdown()
        self._delete_test_log_files()

    def _delete_test_log_files(self):
        """deletes the two generated logfiles"""
        util.remove_file(self._PATH_TO_TEST_DIR + "/" + self._LOG_ERRORS_NAME)
        util.remove_file(self._PATH_TO_TEST_DIR + "/" + self._LOG_INFO_NAME)
