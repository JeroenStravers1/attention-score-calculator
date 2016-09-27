#!/usr/bin/python

import unittest
import types
import os
import sys

sys.path.append("../src")
from head_pose_output_parser import HeadPoseOutputParser
import utils_asc as util

class HeadPoseProcessorTestSuite(unittest.TestCase):
    """contains tests for the head pose output parser module"""

    _TEST_OUTPUT_FILENAME = "test_openface_output.txt"
    _TEST_OPENFACE_OUTPUT_HEADER = "frame, timestamp, confidence, success, pose_Tx, pose_Ty, pose_Tz, pose_Rx, pose_Ry, pose_Rz\n"
    _TEST_OPENFACE_OUTPUT_DATA_1 = "1, 0, 0.941509, 1, -128.26, -210.334, 1020.99, 0.43446, 0.214755, -0.003355\n"
    _TEST_OPENFACE_OUTPUT_DATA_2 = "2, 0.0333333, 0.994467, 1, -3.07635, -785.759, 1714.88, 0.575945, 0.140495, -0.0319438"

    _TYPE_GENERATOR = "<class 'generator'>"

    _EXPECTED_OUTCOMES_X = [0.43446, 0.575945]
    _EXPECTED_OUTCOMES_Y = [0.214755, 0.140495]
    _EXPECTED_OUTCOMES_Z = [-0.003355, -0.0319438]
    _ALL_RESULTS_MATCH = [True, True, True]
    _ALLOWED_DEVIATION = 0.00000001

    def setUp(self):
        self._provision_test_head_pose_processor()
        self._parser = HeadPoseOutputParser()
        self._index_generator = self._parser.extract_valid_head_poses_from_output_file(self._TEST_OUTPUT_FILENAME)
        self._extracted_rx_values = list()
        self._extracted_ry_values = list()
        self._extracted_rz_values = list()

    def _provision_test_head_pose_processor(self):
        """create a test openface output file"""
        output_file_content = self._TEST_OPENFACE_OUTPUT_HEADER + self._TEST_OPENFACE_OUTPUT_DATA_1 + \
                              self._TEST_OPENFACE_OUTPUT_DATA_2
        with open(self._TEST_OUTPUT_FILENAME, 'wb') as output_file:
            util.write_file(bytes(output_file_content, 'UTF-8'), output_file)

    def test_head_pose_output_parser_returns_generator(self):
        """check if head pose output parsing returns a generator object"""
        index_generator_type = str(type(self._index_generator))
        string_generator_types = str(types.GeneratorType)
        self.assertEqual(index_generator_type, string_generator_types)

    def test_head_pose_output_parser_generator_output(self):
        """check if the output of parsing the test output file matches the expected values"""
        self._extract_values()
        comparison_list = list()
        comparison_list.append(self._content_matches(self._extracted_rx_values, self._EXPECTED_OUTCOMES_X))
        comparison_list.append(self._content_matches(self._extracted_ry_values, self._EXPECTED_OUTCOMES_Y))
        comparison_list.append(self._content_matches(self._extracted_rz_values, self._EXPECTED_OUTCOMES_Z))
        all_parsed_results_match_expected_outcomes = self._content_matches(comparison_list, self._ALL_RESULTS_MATCH)
        self.assertTrue(all_parsed_results_match_expected_outcomes)

    def _extract_values(self):
        """store extracted values in arg lists"""
        for rx, ry, rz in self._index_generator:
            self._extracted_rx_values.append(rx)
            self._extracted_ry_values.append(ry)
            self._extracted_rz_values.append(rz)

    def _content_matches(self, parsed_results, expected_results):
        """compares items in a list to items in a list of expected outcomes. Takes into account that they're floats,
        and therefore not necessarily exactly the same."""
        for index, score in enumerate(parsed_results):
            expected_score = expected_results[index]
            if abs(score - expected_score) < self._ALLOWED_DEVIATION:
                return True
            else:
                return False

    def test_output_file_removed(self):
        """tests if the parsed output file has been deleted"""
        output_file_still_exists = os.path.isfile(self._TEST_OUTPUT_FILENAME)
        self.assertFalse(output_file_still_exists)