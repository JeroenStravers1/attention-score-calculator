#!/usr/bin/python

import unittest
import os
import sys

sys.path.append("../src")
import utils_asc as util
from head_pose_processor import HeadPoseProcessor


class HeadPoseProcessorTestSuite(unittest.TestCase):
    """contains tests for the head pose processsor module"""

    _TEST_OUTPUT_FILENAME = "test_openface_output.txt"
    _TEST_OPENFACE_OUTPUT_HEADER = "frame, timestamp, confidence, success, pose_Tx, pose_Ty, pose_Tz, pose_Rx, pose_Ry, pose_Rz\n"
    _TEST_OPENFACE_OUTPUT_DATA_1 = "1, 0, 0.941509, 1, -128.26, -210.334, 1020.99, 0.43446, 0.214755, -0.003355\n"
    _TEST_OPENFACE_OUTPUT_DATA_2 = "2, 0.0333333, 0.994467, 1, -3.07635, -785.759, 1714.88, 0.575945, 0.140495, -0.0319438"

    _PATH_FROM_EXTRACTED_POSES_TO_TEST_OUTPUT_FILE = "../../tests/test_openface_output"
    _EXPECTED_ATTENTION_SCORE = 0

    def setUp(self):
        self._provision_test_head_pose_processor()

    def _provision_test_head_pose_processor(self):
        """initiate the head pose processor object with a path to the test openface output file"""
        output_file_content = self._TEST_OPENFACE_OUTPUT_HEADER + self._TEST_OPENFACE_OUTPUT_DATA_1 + \
                              self._TEST_OPENFACE_OUTPUT_DATA_2
        with open(self._TEST_OUTPUT_FILENAME, 'wb') as output_file:
            util.write_file(bytes(output_file_content, 'UTF-8'), output_file)
        self._processor = HeadPoseProcessor(self._PATH_FROM_EXTRACTED_POSES_TO_TEST_OUTPUT_FILE)

    def test_head_pose_processor_attention_score_calculation(self):
        """check the outcome of attention score calculation on a file with OpenFace head poses"""
        attention_score = self._processor.get_attention_score_from_head_poses()
        self.assertTrue(attention_score == self._EXPECTED_ATTENTION_SCORE)
